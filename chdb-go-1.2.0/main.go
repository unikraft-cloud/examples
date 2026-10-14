package main

import (
	"fmt"
	"os"
	"path/filepath"
	"net/http"

	"github.com/chdb-io/chdb-go/chdb"
)

func query_db(w http.ResponseWriter, req *http.Request) {
	// Stateless Query (ephemeral)
	result, err := chdb.Query("SELECT version()", "CSV")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(result)

	tmp_path := filepath.Join(os.TempDir(), "chdb_test")
	// Stateful Query (persistent)
	session, _ := chdb.NewSession(tmp_path)

	_, err = session.Query("CREATE DATABASE IF NOT EXISTS testdb; " +
		"CREATE TABLE IF NOT EXISTS testdb.testtable (id UInt32) ENGINE = MergeTree() ORDER BY id;")
	if err != nil {
		fmt.Println(err)
		return
	}

	_, err = session.Query("USE testdb; INSERT INTO testtable VALUES (1), (2), (3);")
	if err != nil {
		fmt.Println(err)
		return
	}

	ret, err := session.Query("SELECT * FROM testtable;")
	if err != nil {
		fmt.Fprintf(w, err.Error())
	} else {
		fmt.Fprintf(w, string(ret.Buf()))
	}
}

func main() {
	http.HandleFunc("/", query_db)
	fmt.Println("Listening on :8080...")
	http.ListenAndServe(":8080", nil)
}
