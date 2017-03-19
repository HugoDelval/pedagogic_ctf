package handlers

import (
	"ctf/model"
	"ctf/utils"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"log"
)

var db *gorm.DB

func InitDB(dbType, dataSourceName string) {

	var err error
	db, err = gorm.Open(dbType, dataSourceName)
	if err != nil {
		log.Panic(err)
	}
}

func Migrate() (err error) {

	isProd := utils.GetConfig().IsProduction
	if !isProd {
		db.DropTableIfExists(&model.User{})
		db.DropTableIfExists(&model.Challenge{})
		db.DropTableIfExists(&model.ValidatedChallenge{})
	}

	db.AutoMigrate(&model.User{}, &model.Challenge{}, &model.ValidatedChallenge{})

	return
}
