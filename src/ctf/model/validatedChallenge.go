package model

import (
	"time"
)

type ValidatedChallenge struct {
	ChallengeID   string    `gorm:"primary_key"`
	UserID        string    `gorm:"primary_key"`
	DateValidated time.Time `json:"date_validated"`
}

type ValidatedChallenges []ValidatedChallenge