const express = require('express');
const cors = require('cors');
const { MongoClient, ObjectId } = require('mongodb'); // Importe ObjectId aqui
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 4000;
app.use(cors());
app.use(express.json()); // Add this line to parse JSON data



const uri = "mongodb+srv://trabalhobancodados:DoXnPeOux5FZgnu5@cluster0.jiqhawy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
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

<<<<<<< HEAD
// Nova rota para adicionar livros lidos
app.post('/booksread', async (req, res) => {
  const { email, book } = req.body;
  try {
    const {refIdBook,title, author, description, image, genre } = book; // Extrair os campos do livro
    const bookData = {refIdBook, title, author, description, image, genre }; // Criar um novo objeto livro com esses campos
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

app.get('/books_titulo', async (req, res) => {
  const { title } = req.query;
  try {
    const book = await req.db.collection('books').findOne({ title });
    res.json(book ? [book] : []);
  } catch (error) {
    console.error("Erro ao buscar livro:", error);
    res.status(500).json({ error: "Erro ao buscar livro." });
  }
});

// Adicionar a rota DELETE para excluir um livro
app.delete('/books/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await req.db.collection('books').deleteOne({ _id: new ObjectId(id) });
    if (result.deletedCount === 1) {
      res.status(200).json({ message: 'Livro excluído com sucesso.' });
    } else {
      res.status(404).json({ error: 'Livro não encontrado.' });
    }
  } catch (error) {
    console.error('Erro ao excluir o livro:', error);
    res.status(500).json({ error: 'Erro ao excluir o livro.' });
  }
});

app.delete('/booksread/:email/:id', async (req, res) => {
  const { email, id } = req.params;
  
  try {
    const result = await req.db.collection(`booksread_${email}`).deleteOne({ _id: new ObjectId(id) });
    if (result.deletedCount === 1) {
      res.status(200).json({ message: 'Livro excluído com sucesso.' });
    } else {
      res.status(404).json({ error: 'Livro não encontrado.' });
    }
  } catch (error) {
    console.error('Erro ao excluir o livro:', error);
    res.status(500).json({ error: 'Erro ao excluir o livro.' });
  }
});

=======
>>>>>>> 8421e567bdb7ac13ace21b194f46d56cbd957c82

app.get('/generateRecommendations/:email', async (req, res) => {
  const { email } = req.params;

  try {
    // Buscar todos os livros lidos pelo usuário
    const booksRead = await req.db.collection(`booksread_${email}`).find({}).toArray();
   
    if (booksRead.length === 0) {
      return res.json({ suggestions: [] });
    }
    // Extrair os IDs dos livros lidos e convertê-los para ObjectId
    const readBookIds = booksRead.map(book => new ObjectId(book.refIdBook));

    // Buscar todos os livros disponíveis
    const allBooks = await req.db.collection('books').find({}).toArray();

    if (allBooks.length === 0) {
      return res.json({ suggestions: [] });
    }
    // Filtrar os livros lidos dos livros disponíveis
    const unreadBooks = allBooks.filter(book => !readBookIds.some(readId => readId.equals(book._id)));
    const unreadTitles = unreadBooks.map(book => book.title);

    // Se não houver livros não lidos, retornar uma resposta vazia
    if (unreadTitles.length === 0) {
      return res.json({ suggestions: [] });
    }

    const readTitles = booksRead.map(book => book.title);

    // Se não houver títulos lidos, também retornar uma resposta vazia
    if (readTitles.length === 0) {
      return res.json({ suggestions: [] });
    }

    console.log("Chegou até o comando");

    const process = spawn('python3', ['generate_recommendations.py', JSON.stringify(readTitles), JSON.stringify(unreadTitles)]);

    let dataString = '';

    process.stdout.on('data', (data) => {
      dataString += data.toString();
    });

    process.stdout.on('end', () => {
      try {
        const recommendations = JSON.parse(dataString.replace(/'/g, '"'));
        res.json({ suggestions: recommendations });
      } catch (error) {
        console.error(`Erro ao parsear dados: ${error}`);
        if (!res.headersSent) {
          res.status(500).json({ error: "Erro ao gerar recomendações." });
        }
      }
    });

    process.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      if (!res.headersSent) {
        res.status(500).json({ error: "Erro ao gerar recomendações." });
      }
    });

    process.on('close', (code) => {
      console.log(`Processo finalizado com código ${code}`);
    });

  } catch (error) {
    console.error(`Erro ao buscar dados: ${error}`);
    if (!res.headersSent) {
      res.status(500).json({ error: "Erro ao buscar dados." });
    }
  }
});


app.get('/clusterBooks', async (req, res) => {
  try {
    const books = await req.db.collection('books').find({}).toArray();
    const process = spawn('python3', ['cluster_books.py', JSON.stringify(books)]);

    let dataString = '';

    process.stdout.on('data', (data) => {
      dataString += data.toString();
    });

    process.stdout.on('end', () => {
      try {
        const clusters = JSON.parse(dataString);
        console.log("os clusters", clusters);
        res.json(clusters);
      } catch (error) {
        console.error(`Erro ao parsear dados: ${error}`);
        res.status(500).json({ error: "Erro ao agrupar livros." });
      }
    });

    process.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      res.status(500).json({ error: "Erro ao agrupar livros." });
    });

    process.on('close', (code) => {
      console.log(`Processo finalizado com código ${code}`);
    });

  } catch (error) {
    console.error(`Erro ao buscar dados: ${error}`);
    res.status(500).json({ error: "Erro ao buscar dados." });
  }
});

<<<<<<< HEAD


=======
>>>>>>> 8421e567bdb7ac13ace21b194f46d56cbd957c82
app.listen(port, () => {
  console.log(`Servidor está rodando em http://localhost:${port}`);
});
