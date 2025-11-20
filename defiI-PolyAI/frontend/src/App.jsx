import { useState, useEffect } from "react";
import UploadCard from "./components/UploadCard";
import History from "./components/History";
import axios from "axios";

function App() {
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/history");
      setHistory(res.data);
    } catch (err) {
      console.error("Error fetching history:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-center mb-6">♻️ SmartSort</h1>

      <div className="max-w-xl mx-auto">
        <UploadCard onResult={setResult} refreshHistory={fetchHistory} />
      </div>

      {result && (
        <div className="max-w-xl mx-auto mt-6 p-4 bg-green-100 border border-green-400 rounded">
          <p className="text-xl font-semibold">
            Résultat : <span className="capitalize">{result}</span>
          </p>
        </div>
      )}

      <div className="max-w-2xl mx-auto mt-10">
        <History history={history} />
      </div>
    </div>
  );
}

export default App;
