import { useState } from 'react';
import './App.css';
import sempritoImage from './assets/semprito.png';

function App() {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);

  const handleSend = async () => {
    if (message.trim()) {
      // Adiciona a mensagem do usuário na tela
      setResponses([...responses, { sender: 'Você', text: message }]);

      try {
        // Faz a requisição correta para o backend Flask
        const res = await fetch("http://127.0.0.1:5001/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: message })
        });

        const data = await res.json();

        // Adiciona a resposta da IA na tela
        setResponses(prev => [...prev, { sender: 'Semprito', text: data.reply }]);
      } catch (error) {
        console.error("Erro ao conectar com o backend:", error);
        setResponses(prev => [...prev, { sender: 'Semprito', text: "Erro ao se conectar com o servidor." }]);
      }

      // Limpa a caixa de texto
      setMessage('');
    }
  };

  // Função para detectar a tecla Enter
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="container">
      <h1>Oi!! Eu sou o Semprito, vamos trabalhar com segurança</h1>
      <img src={sempritoImage} alt="Semprito Mascote" className="mascot" />
      
      <div className="chat-box">
        {responses.map((res, index) => (
          <p key={index}><strong>{res.sender}:</strong> {res.text}</p>
        ))}
      </div>

      <div className="input-box">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Digite sua mensagem..."
          onKeyDown={handleKeyPress}  // Detectar pressionamento da tecla Enter
        />
        <button onClick={handleSend}>Enviar</button>
      </div>
    </div>
  );
}

export default App;
