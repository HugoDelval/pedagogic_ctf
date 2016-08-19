package model

import (
	"github.com/jinzhu/gorm"
	"time"
)

type User struct {
	gorm.Model
	Nick                string                `json:"nick" sql:"size:255;unique;index"`
	Password            string                `sql:"size:255" json:"-"`
	IsAdmin             bool                  `json:"-"`
	TimeAuthenticated   time.Time             `json:"-"`
	Token               string                `sql:"size:40" json:"-"`
	ValidatedChallenges []ValidatedChallenge  `json:"validated_challenges"`
}

type Users []User
