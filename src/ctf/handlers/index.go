package handlers

import (
	"net/http"
	"encoding/json"
	"ctf/utils"
	"ctf/model"
	"io/ioutil"
	"log"
)

func Index(w http.ResponseWriter, r *http.Request) {
	// show all challenges
	challengesRaw, err := ioutil.ReadFile(utils.BasePath + "/challenges.json")
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
