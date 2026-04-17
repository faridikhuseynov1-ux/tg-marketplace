import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface Item {
  id: number;
  title: string;
  price: number;
  category: string;
  image: string;
}

export function Marketplace() {
  const [items, setItems] = useState<Item[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

  useEffect(() => {
    fetch(`${API_URL}/items`)
      .then(res => res.json())
      .then(data => {
        setItems(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error("API Error, Fallback triggered:", err);
        setItems([
          { id: 1, title: 'Telegram Premium (MOCK)', price: 29.99, category: 'Services', image: 'https://cdn-icons-png.flaticon.com/512/2111/2111646.png' }
        ]);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-20 gap-3">
        <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-medium">Синхронизация с сервером...</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {['All', 'Premium', 'Digital Trade'].map((cat, i) => (
          <button key={i} className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${i === 0 ? 'bg-blue-500 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>
            {cat}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {items.map((item, index) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            key={item.id} 
            className="bg-slate-800 rounded-2xl p-3 border border-slate-700/50 shadow-sm flex flex-col gap-2 relative overflow-hidden group hover:border-blue-500/50 transition-colors"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 blur-xl rounded-full translate-x-1/2 -translate-y-1/2 group-hover:bg-blue-500/20 transition-colors" />
            
            <div className="aspect-square bg-slate-700/50 rounded-xl flex items-center justify-center p-4">
              <img src={item.image} alt={item.title} className="w-16 h-16 object-contain drop-shadow-lg group-hover:scale-105 transition-transform" />
            </div>
            
            <div className="flex-1 flex flex-col">
              <span className="text-[10px] text-blue-400 font-semibold uppercase tracking-wider">{item.category}</span>
              <h3 className="text-sm font-medium leading-tight mt-1 line-clamp-2">{item.title}</h3>
              <div className="mt-auto pt-3 flex items-center justify-between">
                {/* Интеграция визуала Telegram Stars */}
                <div className="flex items-center gap-1 font-bold text-amber-400 bg-amber-400/10 px-2 py-0.5 rounded-md">
                  <span>⭐️</span>
                  <span>{item.price.toFixed(0)}</span>
                </div>
                <button className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center hover:bg-blue-400 transition-colors shadow-lg shadow-blue-500/20 active:scale-95">
                  +
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
