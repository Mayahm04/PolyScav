import { useState } from "react";
import axios from "axios";

export default function UploadCard({ onResult, refreshHistory }) {
  const [image, setImage] = useState(null);
  const [text, setText] = useState("");

  const handleImagePredict = async () => {
    if (!image) return;
    const formData = new FormData();
    formData.append("file", image);

    const res = await axios.post("http://127.0.0.1:8000/predict/image", formData);
    onResult(res.data.prediction);
    refreshHistory();
  };

  const handleTextPredict = async () => {
    if (!text) return;
    const formData = new FormData();
    formData.append("description", text);

    const res = await axios.post("http://127.0.0.1:8000/predict/text", formData);
    onResult(res.data.prediction);
    refreshHistory();
  };

  return (
    <div className="card">
      <h2 className="text-xl font-bold mb-3">Analyse ton objet</h2>

      <label>Image :</label>
      <input
        type="file"
        onChange={(e) => setImage(e.target.files[0])}
        className="input"
      />

      <button className="btn btn-blue" onClick={handleImagePredict}>
        📸 Prédire via Image
      </button>

      <label>Description :</label>
      <textarea
        placeholder="ex : bouteille plastique"
        className="input"
        onChange={(e) => setText(e.target.value)}
      />

      <button className="btn btn-green" onClick={handleTextPredict}>
        ✍️ Prédire via Texte
      </button>
    </div>
  );
}
