package model

import (
	"github.com/jinzhu/gorm"
)

type User struct {
	gorm.Model
	Nick                string                `json:"nick" sql:"size:255;unique;index"`
	IsAdmin             int                   `json:"is_admin"`
	ValidatedChallenges []ValidatedChallenge
}

type Users []User
