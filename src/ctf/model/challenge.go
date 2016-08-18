package model

import (
	"github.com/jinzhu/gorm"
)

type Challenge struct {
	gorm.Model
	Name        string    `json:"name"` //unique!!
	Points      uint      `json:"points"`
	Description string    `json:"description"`
}

type Challenges []Challenge
