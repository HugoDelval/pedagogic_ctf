package model

import (
	"github.com/jinzhu/gorm"
)

type ChangePassword struct {
	Password            string                `json:"password"`
	PasswordConfirm     string                `json:"passwordConfirm"`
}

type Users []User
