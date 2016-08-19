package handlers 

import (
	"golang.org/x/crypto/bcrypt"
	"time"
	"log"
	"net/http"
	"ctf/utils"
	"ctf/model"
	"errors"
)


func UserRegister(w http.ResponseWriter, r *http.Request) {
	nick := r.FormValue("nick")
	password := r.FormValue("password")

	db, err := model.GetDB(w)
	if err != nil{
		return
	}

	var user model.User
	notFound := db.Where(&model.User{Nick: nick}).First(&user).RecordNotFound()
	if !notFound {
		w.WriteHeader(http.StatusConflict)
		utils.SendResponseJSON(w, utils.Message{"A user with this nick already exists."})
		return
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), 12)
	//err = bcrypt.CompareHashAndPassword(hashedPassword, password)
	if err != nil{
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
		log.Printf("%v\n", err)
		return
	}
	user = model.User{
		Nick: nick,
		Password: string(hashedPassword),
		IsAdmin: false,
	}

	db.Create(&user)

	w.WriteHeader(http.StatusCreated)
	utils.SendResponseJSON(w, utils.Message{"User successfully created."})
}

func AuthenticateUser(w http.ResponseWriter, r *http.Request){
	nick := r.FormValue("nick")
	password := r.FormValue("password")

	db, err := model.GetDB(w)
	if err != nil{
		return
	}

	var user model.User
	notFound := db.Where(&model.User{Nick: nick}).First(&user).RecordNotFound()
	if notFound{
		w.WriteHeader(http.StatusUnauthorized)
		utils.SendResponseJSON(w, utils.Message{"Can't login with those credentials."})
		log.Printf("%v\n", err)
		return 
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password))
	if err != nil{
		w.WriteHeader(http.StatusUnauthorized)
		utils.SendResponseJSON(w, utils.Message{"Can't login with those credentials."})
		log.Printf("%v\n", err)
		return
	}

	currentTime := time.Now()
	user.TimeAuthenticated = currentTime
	user.Token = utils.RandString(40)

	db.Save(&user)

	w.WriteHeader(http.StatusAccepted)
	utils.SendResponseJSON(w, user.Token)
}

func IsUserAuthenticated(w http.ResponseWriter, r *http.Request) (registeredUser bool, user model.User, err error){
	token := r.Header.Get("X-CTF-AUTH")
	registeredUser = false
	
	if token == ""{
		return
	}

	db, err := model.GetDB(w)
	if err != nil {return}

	notFound := db.Where(&model.User{Token: token}).First(&user).RecordNotFound()
	if notFound {
		return 
	}

	hoursElapsed := time.Now().Sub(user.TimeAuthenticated).Hours()
	if hoursElapsed > 48 { return registeredUser, user, errors.New("Token timed out.") }
	registeredUser = true

	return 
}

