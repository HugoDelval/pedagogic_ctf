package model

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"log"
	"ctf/utils"
)

func GetDB() (db *gorm.DB, err error)  {
	db, err = gorm.Open("sqlite3", "database.db")
	if err != nil {
		log.Printf("Failed to connect database : %v", err)
	}
	return
}

func Migrate() (err error){
	db, err := GetDB()
	if err!= nil{
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