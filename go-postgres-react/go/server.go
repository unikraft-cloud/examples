package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"

	_ "github.com/lib/pq"
)

type Contact struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

var db *sql.DB

func main() {
	var err error
	db, err = sql.Open(
		"postgres",
		"user=postgres dbname=postgres password=unikraft host=postgres-wahr0.internal sslmode=disable",
	)
	if err != nil {
		panic(err)
	}

	http.HandleFunc("/contacts", contactsHandler)

	fmt.Println("Listening on :8080...")
	http.ListenAndServe(":8080", nil)
}

func contactsHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		rows, err := db.Query("SELECT name, email FROM contacts")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		defer rows.Close()

		var contacts []Contact
		for rows.Next() {
			var c Contact
			if err := rows.Scan(&c.Name, &c.Email); err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			contacts = append(contacts, c)
		}

		json.NewEncoder(w).Encode(contacts)
	case http.MethodPost:
		var c Contact
		json.NewDecoder(r.Body).Decode(&c)

		_, err := db.Exec(
			"INSERT INTO contacts(name, email) VALUES($1, $2)",
			c.Name,
			c.Email,
		)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		json.NewEncoder(w).Encode(c)
	default:
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
	}
}
