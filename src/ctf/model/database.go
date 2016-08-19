package model

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"log"
	"ctf/utils"
	"net/http"
)

func getDB()(db *gorm.DB, err error){
	db, err = gorm.Open("sqlite3", "database.db")
	return
}

func GetDB(w http.ResponseWriter) (db *gorm.DB, err error)  {
	db, err = getDB()
	if err != nil {
		log.Printf("Failed to connect database : %v", err)
		w.WriteHeader(http.StatusInternalServerError)
		utils.SendResponseJSON(w, utils.InternalErrorMessage)
	}
	return
}

func Migrate() (err error){
	db, err := getDB()
	if err != nil{
		return
	}

	isProd := utils.GetConfig().IsProduction
	if !isProd{
		db.DropTableIfExists(&User{})
		db.DropTableIfExists(&Challenge{})
		db.DropTableIfExists(&ValidatedChallenge{})
	}

	db.AutoMigrate(&User{}, &Challenge{}, &ValidatedChallenge{})

	return
}