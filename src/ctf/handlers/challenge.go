package handlers

import (
	"net/http"
	"encoding/json"
	"ctf/utils"
	"ctf/model"
	"io/ioutil"
	"log"
	"fmt"
	"github.com/gorilla/mux"
	"strconv"
	"os"
	"os/exec"
	"time"
	"errors"
	"regexp"
	"path/filepath"
)

// exists returns whether the given file or directory exists or not
func exists(path string) (bool, error) {
    _, err := os.Stat(path)
    if err == nil { return true, nil }
    if os.IsNotExist(err) { return false, nil }
    return true, err
}


func customCommand(name string, dir string, arg ...string) *exec.Cmd {
	cmd := &exec.Cmd{
				Path: name,
				Args: append([]string{name}, arg...),
				Dir: dir,
	}
	if filepath.Base(name) == name {
		if lp, err := exec.LookPath(name); err == nil {
			cmd.Path = lp
		}
	}
	return cmd
}


func getChallengeInfos(w http.ResponseWriter, r *http.Request) (challengeName string, challengeFolderPath string, challenge model.Challenge, err error){
	vars := mux.Vars(r)
	challengeName = vars["challengeName"]

	regexChallName := regexp.MustCompile(`^[\w-]+$`)
	if !regexChallName.MatchString(challengeName){
	    w.WriteHeader(http.StatusNotFound)
	    utils.SendResponseJSON(w, utils.NotFoundErrorMessage)
	    err = errors.New("Challenge name not valid.")
	    return
	}

	challengeFolderPath = utils.BasePath + utils.ChallengeFolder + challengeName + ".dir/"
	exists, err := exists(challengeFolderPath)
	if !exists || err != nil{
	    w.WriteHeader(http.StatusNotFound)
    	utils.SendResponseJSON(w, utils.NotFoundErrorMessage)
    	if err == nil{
	    	err = errors.New("File Not Found.")
	    }else{
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
	if err != nil{
		return
	}

	for index, language := range challenge.Languages{
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
	if err != nil{
		return
	}
	var secretRaw []byte
	var secretJSON map[string]*json.RawMessage
	if err := utils.LoadJSONFromRequest(w, r, &secretRaw); err != nil{
		return
	}
	if err := json.Unmarshal(secretRaw, &secretJSON); err != nil{
		w.WriteHeader(http.StatusBadRequest)
		utils.SendResponseJSON(w, utils.BadRequestMessage)
		log.Println(err)
		return
	}

	secret := ""
	secretJSONVal, ok := secretJSON["secret"];
	if(ok){
		if err := json.Unmarshal(*secretJSONVal, &secret); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			utils.SendResponseJSON(w, utils.BadRequestMessage)
			log.Println(err)
			return
		}
	}
	realSecret, err := ioutil.ReadFile(challengeFolderPath + utils.FlagFileName)
	if secret != string(realSecret[:]){
		w.WriteHeader(http.StatusNotAcceptable)
		utils.SendResponseJSON(w, utils.Message{"Not the good secret sorry. Be carefull with spaces when copy-pasting."})
		return
	}

	registeredUser, user, err := IsUserAuthenticated(w, r)
	if err != nil {
		return
	}else if !registeredUser{
		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You did not earned any points because you're not logged in.\n" + challenge.ResolvedConclusion})
	}else{
		newValidatedChall := model.ValidatedChallenge{
			ChallengeID: challengeName,
			UserID: strconv.Itoa(int(user.ID)),
			DateValidated: time.Now(),
		}
		db, err := model.GetDB(w)
		if err != nil {return}

		var alreadyValidated model.ValidatedChallenge
		notFound := db.Where(&model.ValidatedChallenge{ChallengeID: challengeName, UserID: strconv.Itoa(int(user.ID))}).First(&alreadyValidated).RecordNotFound()
		if !notFound{
			w.WriteHeader(http.StatusNotAcceptable)
			utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) But you already validated this challenge, so no points this time.\n" + challenge.ResolvedConclusion})
			return
		}

		if err := db.Create(&newValidatedChall).Error; err != nil{
			w.WriteHeader(http.StatusInternalServerError)
			utils.SendResponseJSON(w, utils.InternalErrorMessage)
			log.Printf("%v\n", err)
			return
		}

		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You earned " + strconv.Itoa(int(challenge.Points)) + "pts for that.\n" + challenge.ResolvedConclusion})
	}
}


func ChallengeExecute(w http.ResponseWriter, r *http.Request) {
	_, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil{
		return
	}

	var paramsRaw []byte
	var paramsJSON map[string]*json.RawMessage
	if err := utils.LoadJSONFromRequest(w, r, &paramsRaw); err != nil{
		return
	}
	_ = json.Unmarshal(paramsRaw, &paramsJSON)

	args := make([]string, len(challenge.Parameters))
	for index, arg := range challenge.Parameters{
		paramJSONVal, ok := paramsJSON[arg.Name];
		if !ok {
		    args[index] = ""
		    continue
		}
		if err := json.Unmarshal(*paramJSONVal, &(args[index])); err != nil{
			args[index] = ""
		}
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

func ChallengeShowAll(w http.ResponseWriter, r *http.Request) {
	challengesPath := utils.BasePath + "challenges.json"
	
	challengesRaw, err := ioutil.ReadFile(challengesPath)
    if err != nil {
	    w.WriteHeader(http.StatusInternalServerError)
    	utils.SendResponseJSON(w, utils.InternalErrorMessage)
        log.Printf("File error: %v\n", err)
        return
    }

    var challenges model.Challenges
	err = json.Unmarshal(challengesRaw, &challenges)
	if err != nil {
        w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
        log.Printf("File error: %v\n", err)
        return
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenges)
}