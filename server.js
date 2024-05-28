const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');

const app = express();
const port = process.env.PORT || 4000;
app.use(cors());
app.use(express.json()); // Add this line to parse JSON data

const uri = process.env.URL;
const client = new MongoClient(uri);

app.use(async (req, res, next) => {
  try {
    await client.connect();
    console.log("Conectado ao MongoDB Atlas!");
    req.db = client.db();
    next();
  } catch (error) {
    console.error("Erro ao conectar ao MongoDB Atlas:", error);
    res.status(500).json({ error: "Erro ao conectar ao banco de dados." });
  }
});

app.get('/books', async (req, res) => {
  try {
    const books = await req.db.collection('books').find({}).toArray();
    res.json(books);
  } catch (error) {
    console.error("Erro ao buscar livros:", error);
    res.status(500).json({ error: "Erro ao buscar livros." });
  }
});

app.post('/books', async (req, res) => {
  try {
    const newBook = req.body; // Access request body
    await req.db.collection('books').insertOne(newBook);
    res.status(201).json(newBook);
  } catch (error) {
    console.error("Erro ao adicionar um novo livro ao acervo:", error);
    res.status(500).json({ error: "Erro ao adicionar um novo livro ao acervo." });
  }
});


// Nova rota para adicionar livros lidos
app.post('/booksread', async (req, res) => {
    const { email, book } = req.body;
    try {
      const { title, author, description, image, genre } = book; // Extrair os campos do livro
      const bookData = { title, author, description, image, genre }; // Criar um novo objeto livro com esses campos
      await req.db.collection(`booksread_${email}`).insertOne(bookData);
      res.status(201).json(bookData);
    } catch (error) {
      console.error("Erro ao adicionar um novo livro ao acervo:", error);
      res.status(500).json({ error: "Erro ao adicionar um novo livro ao acervo." });
    }
  });
  

// Nova rota para buscar livros lidos por um usuário
app.get('/booksread/:email', async (req, res) => {
  const { email } = req.params;
  try {
    const booksRead = await req.db.collection(`booksread_${email}`).find({}).toArray();
    res.json(booksRead);
  } catch (error) {
    console.error("Erro ao buscar livros lidos:", error);
    res.status(500).json({ error: "Erro ao buscar livros lidos." });
  }
});


app.listen(port, () => {
  console.log(`Servidor está rodando em http://localhost:${port}`);
});
