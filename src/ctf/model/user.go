package model

import (
	"github.com/jinzhu/gorm"
	"time"
)

type UserValidatedChallenge struct {
	ChallengeName string    `json:"name"`
	Exploited     bool      `json:"is_exploited"`
	Corrected     bool      `json:"is_corrected"`
	Points        int       `json:"points"`
	DateValidated time.Time `json:"date_validated"`
}

type UserCTFResult struct {
	Id        int    `json:"id"`
	Email     string `json:"email"`
	Exploited int    `json:"exploited"`
	Corrected int    `json:"corrected"`
	Points    int    `json:"points"`
}

type User struct {
	gorm.Model
	Email             string    `json:"email" sql:"size:255;unique;index"`
	Password          string    `sql:"size:255" json:"password,omitempty"`
	IsAdmin           bool      `json:"-"`
	TimeAuthenticated time.Time `json:"-"`
	Token             string    `sql:"size:40" json:"-"`
}

type Users []User
