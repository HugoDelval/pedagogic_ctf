package handlers

import (
	"ctf/model"
	"ctf/utils"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gorilla/mux"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strconv"
	"time"
)

// exists returns whether the given file or directory exists or not
func exists(path string) (bool, error) {
	_, err := os.Stat(path)
	if err == nil {
		return true, nil
	}
	if os.IsNotExist(err) {
		return false, nil
	}
	return true, err
}

func customCommand(name string, dir string, arg ...string) *exec.Cmd {
	cmd := &exec.Cmd{
		Path: name,
		Args: append([]string{name}, arg...),
		Dir:  dir,
	}
	if filepath.Base(name) == name {
		if lp, err := exec.LookPath(name); err == nil {
			cmd.Path = lp
		}
	}
	return cmd
}

func getChallengeInfos(w http.ResponseWriter, r *http.Request) (challengeName string, challengeFolderPath string, challenge model.Challenge, err error) {
	vars := mux.Vars(r)
	challengeName = vars["challengeName"]

	regexChallName := regexp.MustCompile(`^[\w-]+$`)
	if !regexChallName.MatchString(challengeName) {
		w.WriteHeader(http.StatusNotFound)
		utils.SendResponseJSON(w, utils.NotFoundErrorMessage)
		err = errors.New("Challenge name not valid.")
		return
	}

	challengeFolderPath = utils.BasePath + utils.ChallengeFolder + challengeName + ".dir/"
	exists, err := exists(challengeFolderPath)
	if !exists || err != nil {
		w.WriteHeader(http.StatusNotFound)
		utils.SendResponseJSON(w, utils.NotFoundErrorMessage)
		if err == nil {
			err = errors.New("File Not Found.")
		} else {
			log.Printf("Cannot find folder : %v\n", err)
		}
		return
	}

	challengeJSON := challengeFolderPath + challengeName + ".json"
	challengeRaw, err := ioutil.ReadFile(challengeJSON)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Printf("File error: %v\n", err)
		return
	}

	err = json.Unmarshal(challengeRaw, &challenge)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Printf("File error: %v\n", err)
		return
	}
	return
}

func ChallengeShow(w http.ResponseWriter, r *http.Request) {
	challengeName, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil {
		return
	}

	for index, language := range challenge.Languages {
		challengeFilePath := challengeFolderPath + challengeName + language.Extension
		challengeContent, err := ioutil.ReadFile(challengeFilePath)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			utils.SendResponseJSON(w, utils.InternalErrorMessage)
			log.Printf("File error: %v\n", err)
			return
		}
		challenge.Languages[index].FileContent = string(challengeContent[:])
	}

	challenge.ResolvedConclusion = ""

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenge)
}

func ChallengeValidate(w http.ResponseWriter, r *http.Request) {
	challengeName, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil {
		return
	}
	var secretRaw []byte
	var secretJSON map[string]*json.RawMessage
	if err := utils.LoadJSONFromRequest(w, r, &secretRaw); err != nil {
		return
	}
	if err := json.Unmarshal(secretRaw, &secretJSON); err != nil {
		w.WriteHeader(http.StatusBadRequest)
		utils.SendResponseJSON(w, utils.BadRequestMessage)
		log.Println(err)
		return
	}

	secret := ""
	secretJSONVal, ok := secretJSON["secret"]
	if ok {
		if err := json.Unmarshal(*secretJSONVal, &secret); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			utils.SendResponseJSON(w, utils.BadRequestMessage)
			log.Println(err)
			return
		}
	}
	realSecret, err := ioutil.ReadFile(challengeFolderPath + utils.FlagFileName)
	if secret != string(realSecret[:]) {
		w.WriteHeader(http.StatusNotAcceptable)
		utils.SendResponseJSON(w, utils.Message{"Not the good secret sorry. Be carefull with spaces when copy-pasting."})
		return
	}

	registeredUser, user, err := IsUserAuthenticated(w, r)
	if err != nil {
		return
	} else if !registeredUser {
		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You did not earned any points because you're not logged in.\n" + challenge.ResolvedConclusion})
		return
	} else {

		var alreadyValidated model.ValidatedChallenge
		notFound := db.Where(&model.ValidatedChallenge{ChallengeID: challengeName, UserID: strconv.Itoa(int(user.ID))}).First(&alreadyValidated).RecordNotFound()
		if !notFound && alreadyValidated.IsExploited {
			w.WriteHeader(http.StatusNotAcceptable)
			utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) But you already exploited this challenge, so no points this time.\n" + challenge.ResolvedConclusion})
			return
		}

		if !notFound {
			// we found the validatedChallenge object but it wasn't exploited (the user just corrected the challenge, and now he exploits it)
			alreadyValidated.IsExploited = true
			if err := db.Save(&alreadyValidated).Error; err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				utils.SendResponseJSON(w, utils.InternalErrorMessage)
				log.Printf("%v\n", err)
				return
			}
		} else {
			newValidatedChall := model.ValidatedChallenge{
				ChallengeID:   challengeName,
				UserID:        strconv.Itoa(int(user.ID)),
				IsExploited:   true,
				IsCorrected:   false,
				DateValidated: time.Now(),
			}
			// this is a new validatedChallenge
			if err := db.Create(&newValidatedChall).Error; err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				utils.SendResponseJSON(w, utils.InternalErrorMessage)
				log.Printf("%v\n", err)
				return
			}
		}

		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You earned " + strconv.Itoa(int(challenge.Points)) + "pts for that.\n" + challenge.ResolvedConclusion})
	}
}

func ChallengeExecute(w http.ResponseWriter, r *http.Request) {
	challengeName, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil {
		return
	}

	// TODO: change Challenge Model
	authenticatedCahllenges := map[string]bool{
		"stored_xss": true,
	}

	registeredUser, user, _ := IsUserAuthenticated(w, r)
	if !registeredUser && authenticatedCahllenges[challengeName] {
		w.WriteHeader(http.StatusForbidden)
		utils.SendResponseJSON(w, utils.Message{"You need to be logged in to execute this challenge"})
		return
	}

	var paramsRaw []byte
	var paramsJSON map[string]*json.RawMessage
	if err := utils.LoadJSONFromRequest(w, r, &paramsRaw); err != nil {
		return
	}
	_ = json.Unmarshal(paramsRaw, &paramsJSON)

	args := make([]string, len(challenge.Parameters), len(challenge.Parameters)+1)

	for index, arg := range challenge.Parameters {
		paramJSONVal, ok := paramsJSON[arg.Name]
		if !ok {
			args[index] = ""
			continue
		}
		if err := json.Unmarshal(*paramJSONVal, &(args[index])); err != nil {
			args[index] = ""
		}
	}

	if authenticatedCahllenges[challengeName] { // Inject User email
		args = append([]string{user.Email}, args...)
	}

	cmd := challengeFolderPath + "wrapper"
	out, err := customCommand(cmd, challengeFolderPath, args...).CombinedOutput()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		encouragingMessage := fmt.Sprintf("Mmmh.. Looks like your request failed.. You might be on the good track. Here is your error : \"%v : %s\"", err, string(out[:]))
		utils.SendResponseJSON(w, utils.Message{encouragingMessage})
		log.Printf("%v : %s\n", err, string(out[:]))
		return
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, utils.Message{string(out[:])})
}

func ChallengeCorrect(w http.ResponseWriter, r *http.Request) {
	challengeName, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil {
		return
	}

	var correctedScript model.CorrectedScript
	var correctedScriptRaw []byte
	err = utils.LoadJSONFromRequest(w, r, &correctedScriptRaw)
	if err != nil {
		return
	}
	err = json.Unmarshal(correctedScriptRaw, &correctedScript)
	if err != nil {
		utils.SendResponseJSON(w, utils.BadRequestMessage)
		log.Println(err)
		return
	}

	// TODO: Security, match available challenge extensions (avoid .sh injection for example)
	regexLanguageExtension := regexp.MustCompile(`^\.[a-z0-9]{2,5}$`)
	if !regexLanguageExtension.MatchString(correctedScript.LanguageExtension) {
		w.WriteHeader(http.StatusBadRequest)
		utils.SendResponseJSON(w, utils.BadRequestMessage)
		return
	}

	// mkdir random folder + create script file based on user input
	correctedScriptPath := "/srv/writable/" + challengeName + "_" + utils.RandString(30) + "/"
	if err = os.Mkdir(correctedScriptPath, 0750); err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Println(err)
		return
	}
	scriptFile, err := os.Create(correctedScriptPath + challengeName + correctedScript.LanguageExtension)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Println(err)
		return
	}
	_, err = scriptFile.WriteString(correctedScript.ContentScript)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Println(err)
		return
	}
	scriptFile.Sync()
	scriptFile.Close()

	cmd := utils.BasePath + "check_challenge_corrected"
	out, err := customCommand(cmd, challengeFolderPath, correctedScriptPath, challengeName, correctedScript.LanguageExtension).CombinedOutput()
	if err != nil {
		w.WriteHeader(http.StatusNotAcceptable)
		encouragingMessage := fmt.Sprintf("Mmmh.. Looks like your script is not perfect yet.. Here is your error : \"%v : %s\"", err, string(out[:]))
		utils.SendResponseJSON(w, utils.Message{encouragingMessage})
		log.Printf("%v : %s\n", err, string(out[:]))
		return
	}

	registeredUser, user, err := IsUserAuthenticated(w, r)
	if err != nil {
		return
	} else if !registeredUser {
		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You did not earned any points because you're not logged in.\n" + challenge.ResolvedConclusion})
	} else {

		var alreadyValidated model.ValidatedChallenge
		notFound := db.Where(&model.ValidatedChallenge{ChallengeID: challengeName, UserID: strconv.Itoa(int(user.ID))}).First(&alreadyValidated).RecordNotFound()
		if !notFound && alreadyValidated.IsCorrected {
			w.WriteHeader(http.StatusNotAcceptable)
			utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) But you already corrected this challenge, so no points this time.\n" + challenge.ResolvedConclusion})
			return
		}

		if !notFound {
			// we found the validatedChallenge object but it wasn't corrected (the user just exploited the challenge, and now he corrects it)
			alreadyValidated.IsCorrected = true
			if err := db.Save(&alreadyValidated).Error; err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				utils.SendResponseJSON(w, utils.InternalErrorMessage)
				log.Printf("%v\n", err)
				return
			}
		} else {
			newValidatedChall := model.ValidatedChallenge{
				ChallengeID:   challengeName,
				UserID:        strconv.Itoa(int(user.ID)),
				IsExploited:   false,
				IsCorrected:   true,
				DateValidated: time.Now(),
			}
			// this is a new validatedChallenge
			if err := db.Create(&newValidatedChall).Error; err != nil {
				w.WriteHeader(http.StatusInternalServerError)
				utils.SendResponseJSON(w, utils.InternalErrorMessage)
				log.Printf("%v\n", err)
				return
			}
		}
		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You earned " + strconv.Itoa(int(challenge.Points)) + "pts for that.\n" + challenge.ResolvedConclusion})
	}
}

func GetChallenges() (challenges model.Challenges, err error) {

	challengesPath := utils.BasePath + "challenges.json"

	challengesRaw, err := ioutil.ReadFile(challengesPath)
	if err != nil {
		log.Printf("File error: %v\n", err)
		return
	}

	err = json.Unmarshal(challengesRaw, &challenges)
	if err != nil {
		log.Printf("File error: %v\n", err)
		return
	}
	return challenges, err
}

func ChallengeShowAll(w http.ResponseWriter, r *http.Request) {

	challenges, err := GetChallenges()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		return
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenges)
}
