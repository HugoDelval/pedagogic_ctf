package handlers

import (
	"ctf/model"
	"ctf/utils"
	"net/http"
	"strconv"
)

type ChallengeResult struct {
	Exploited bool `gorm:"column:is_exploited"`
	Corrected bool `gorm:"column:is_corrected"`
}

type UserResult struct {
	Id        int    `json:"id"`
	Email     string `json:"email"`
	Exploited int    `json:"exploited"`
	Corrected int    `json:"corrected"`
	Points    int    `json:points"`
}

type Scoreboard []UserResult

func Index(w http.ResponseWriter, r *http.Request) {
	// show all challenges
	challenges, err := GetChallenges()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		return
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, challenges)
}

func GetScoreboard(w http.ResponseWriter, r *http.Request) {
	// Get scoreboard

	db, err := model.GetDB(w)
	if err != nil {
		return
	}

	challenges, err := GetChallenges()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		return
	}

	challengesPoints := make(map[string]int)
	for _, challenge := range challenges {
		challengesPoints[challenge.ChallengeId] = int(challenge.Points)
	}

	var users model.Users
	db.Find(&users)

	scoreboard := Scoreboard{}

	for _, user := range users {

		var totalCorrected int
		var totalExploited int
		var totalPoints int

		var validatedChallenges model.ValidatedChallenges
		userId := strconv.FormatUint(uint64(user.ID), 10)
		db.Where(&model.ValidatedChallenge{UserID: userId}).Find(&validatedChallenges)

		for _, challenge := range validatedChallenges {

			if challenge.IsCorrected {
				totalCorrected += 1
			}

			if challenge.IsExploited {
				totalExploited += 1
			}

			if challenge.IsExploited && challenge.IsCorrected {
				totalPoints += challengesPoints[challenge.ChallengeID]
			}
		}

		result := UserResult{
			Id:        int(user.ID),
			Email:     user.Email,
			Exploited: totalExploited,
			Corrected: totalCorrected,
			Points:    totalPoints,
		}

		scoreboard = append(scoreboard, result)
	}

	w.WriteHeader(http.StatusOK)
	utils.SendResponseJSON(w, scoreboard)
}
