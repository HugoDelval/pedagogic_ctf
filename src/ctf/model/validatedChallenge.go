package model

import (
	"time"
)

type ValidatedChallenge struct {
	ChallengeID   string    `gorm:"primary_key"`
	UserID        string    `gorm:"primary_key"`
	IsCorrected   bool      `json:"is_corrected"`
	IsExploited   bool      `json:"is_exploited"`
	DateValidated time.Time `json:"date_validated"`
}

type ValidatedChallenges []ValidatedChallenge