package handlers

import (
	"net/http"
	"ctf/utils"
	"ctf/model"
)

func Index(w http.ResponseWriter, r *http.Request) {
	// create challenge + show all challenges
	chall := model.Challenge{Name: "TestChall", Points: 18, Description: "test"}
	db, err := model.GetDB()
	if err != nil{
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	db.Create(&chall)

	var challenges model.Challenges
	db.Find(&challenges)
	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenges)
}
