body {
  font-family: Arial;
  background: #eef2f5;
  padding: 20px;
}

h1 {
  text-align: center;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  padding: 15px;
  border-radius: 10px;
}

button {
  margin: 5px;
  padding: 8px;
  border: none;
  cursor: pointer;
  color: white;
}

.accept { background: green; }
.pick { background: orange; }
.deliver { background: blue; }