package main

import (
	"fmt"
	"net/http"
	"os"
)

// The handler responds with the current instance's hostname.
// Under heavy load, when the autoscaler creates clones, we will see different hostnames here.
func handler(w http.ResponseWriter, r *http.Request) {
	hostname, _ := os.Hostname()
	fmt.Fprintf(w, "Hello from KraftCloud! Responding instance: %s\n", hostname)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Server starting on port 8080...")
	http.ListenAndServe(":8080", nil)
}
