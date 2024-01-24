package main

import (
	"database/sql"
	"fmt"

	_ "github.com/marcboeker/go-duckdb"
)

func main() {
	db, _ := sql.Open("duckdb", "")

	db.Exec(`CREATE TABLE person (id INTEGER, name VARCHAR)`)
	db.Exec(`INSERT INTO person VALUES (42, 'John')`)

	var (
		id   int
		name string
	)
	row := db.QueryRow(`SELECT id, name FROM person`)
	_ = row.Scan(&id, &name)
	fmt.Println("id:", id, "name:", name)
}
