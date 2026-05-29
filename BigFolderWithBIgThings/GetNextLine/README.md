*This project has been created as part of the 42 curriculum by rafmonte*

---Description---
This project is a function that reads and returns text from a file descriptor, one line at a time. The functions keeps track of where it stopped between calls, allowing it to pick up where it left off when called again.

---Instructions---
To use this function, open your file using the open() function, call get next line to read a line from said file, free the line to avoid memory leaks and close the file when you're finished with it.

---Resources---
AI was used in this project to better understand topics related to it such as static variables and file management.

---Algorithm---
This implementation of get next line uses a buffer that persists between calls to remember where it stopped reading after the last call and separates the steps required to make the reading process work(reading, extracting lines and buffer management) into different functions to maintain an organized structure.
