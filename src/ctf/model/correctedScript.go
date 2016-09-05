package model

type CorrectedScript struct{
	LanguageExtension   string       `json:"language_extension"` // ex : .py or .go
	ContentScript       string       `json:"content_script"`
}
