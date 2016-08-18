package handlers

import (
	"net/http"
	"encoding/json"
	"ctf/utils"
	"ctf/model"
	"io/ioutil"
	"log"
	"github.com/gorilla/mux"
	"os"
)

// exists returns whether the given file or directory exists or not
func exists(path string) (bool, error) {
    _, err := os.Stat(path)
    if err == nil { return true, nil }
    if os.IsNotExist(err) { return false, nil }
    return true, err
}


func ChallengeShow(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	challengeName := vars["challengeName"]

	challengeFolderPath := utils.BasePath + utils.ChallengeFolder + challengeName + ".dir/"
	if exists, err := exists(challengeFolderPath); !exists || err != nil{
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

    var challenge model.Challenge
	err = json.Unmarshal(challengeRaw, &challenge)
	if err != nil {
        w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
        log.Printf("File error: %v\n", err)
        return
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenge)
}
