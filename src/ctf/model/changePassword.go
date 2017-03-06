package model

type ChangePassword struct {
	Password            string                `json:"password"`
	PasswordConfirm     string                `json:"passwordConfirm"`
}
