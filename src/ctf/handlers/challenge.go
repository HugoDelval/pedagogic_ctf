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
)

// exists returns whether the given file or directory exists or not
func exists(path string) (bool, error) {
    _, err := os.Stat(path)
    if err == nil { return true, nil }
    if os.IsNotExist(err) { return false, nil }
    return true, err
}


func getChallengeInfos(w http.ResponseWriter, r *http.Request) (challengeName string, challengeFolderPath string, challenge model.Challenge, err error){
	vars := mux.Vars(r)
	challengeName = vars["challengeName"]

	challengeFolderPath = utils.BasePath + utils.ChallengeFolder + challengeName + ".dir/"
	exists, err := exists(challengeFolderPath)
	if !exists || err != nil{
	    w.WriteHeader(http.StatusNotFound)
    	utils.SendResponseJSON(w, utils.NotFoundErrorMessage)
        log.Printf("Cannot find folder : %v\n", err)
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

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenge)
}

func ChallengeValidate(w http.ResponseWriter, r *http.Request) {
	challengeName, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil{
		return
	}
	secret := r.FormValue("secret")
	realSecret, err := ioutil.ReadFile(challengeFolderPath + utils.FlagFileName)
	if secret != string(realSecret[:]){
		w.WriteHeader(http.StatusForbidden)
		utils.SendResponseJSON(w, utils.Message{"Not the good secret sorry. Be carefull with spaces when copy-pasting."})
		return
	}

	registeredUser, user, err := IsUserAuthenticated(w, r)
	if err != nil {
		return
	}else if !registeredUser{
		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You did not earned any points because you're not logged in."})
	}else{
		newValidatedChall := model.ValidatedChallenge{
			ChallengeID: challengeName,
			User: user,
			UserID: strconv.Itoa(int(user.ID)),
			DateValidated: time.Now(),
		}
		db, err := model.GetDB(w)
		if err != nil {return}

		var alreadyValidated model.ValidatedChallenge
		notFound := db.Where(&model.ValidatedChallenge{ChallengeID: challengeName, UserID: strconv.Itoa(int(user.ID))}).First(&alreadyValidated).RecordNotFound()
		if !notFound{
			w.WriteHeader(http.StatusNotAcceptable)
			utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) But you already validated this challenge, so no points this time."})
			return
		}

		if err := db.Create(&newValidatedChall).Error; err != nil{
			w.WriteHeader(http.StatusInternalServerError)
			utils.SendResponseJSON(w, utils.InternalErrorMessage)
			log.Printf("%v\n", err)
			return
		}

		w.WriteHeader(http.StatusOK)
		utils.SendResponseJSON(w, utils.Message{"Congratz !! You did it :) You earned " + strconv.Itoa(int(challenge.Points)) + "pts for that."})
	}
}


func ChallengeExecute(w http.ResponseWriter, r *http.Request) {
	_, challengeFolderPath, challenge, err := getChallengeInfos(w, r)
	if err != nil{
		return
	}

	args := make([]string, len(challenge.Parameters))
	for index, arg := range challenge.Parameters{
		args[index] = r.FormValue(arg.Name)
	}

	cmd := challengeFolderPath + "wrapper"
	out, err := exec.Command(cmd, args...).CombinedOutput()
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

