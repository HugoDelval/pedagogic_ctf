package model

import (
	"github.com/jinzhu/gorm"
	"time"
)

type User struct {
	gorm.Model
	Email             string    `json:"email" sql:"size:255;unique;index"`
	Password          string    `sql:"size:255" json:"password,omitempty"`
	IsAdmin           bool      `json:"-"`
	TimeAuthenticated time.Time `json:"-"`
	Token             string    `sql:"size:40" json:"-"`
}

type Users []User
