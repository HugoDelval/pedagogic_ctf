package model

import (
	"time"
)

type ValidatedChallenge struct {
	Challenge     Challenge `gorm:"AssociationForeignKey:ChallengeID"`
	ChallengeID   string    `gorm:"primary_key"`
	User          User      `gorm:"AssociationForeignKey:UserID"`
	UserID        string    `gorm:"primary_key"`
	DateValidated time.Time `json:"date_validated"`
// add unique between challenge and user
}

