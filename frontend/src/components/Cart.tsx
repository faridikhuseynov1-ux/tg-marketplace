import { useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, ArrowRight, Loader2 } from 'lucide-react';
import WebApp from '@twa-dev/sdk';

export function Cart() {
  const [isProcessing, setIsProcessing] = useState(false);

  // JWT Auth Handler
  const getAuthToken = async () => {
    let token = sessionStorage.getItem('jwt_token');
    if (token) return token;
    
    try {
      const initData = WebApp.initData;
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
      const res = await fetch(`${API_URL}/auth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ initData })
      });
      const data = await res.json();
      if (data.access_token) {
        sessionStorage.setItem('jwt_token', data.access_token);
        return data.access_token;
      }
    } catch(e) {
      console.warn("Auth network error (Fallback running)");
    }
    return '';
  };

  const handleCheckout = async () => {
    WebApp.HapticFeedback.impactOccurred('medium');
    WebApp.showConfirm('Заключить Safe Deal (Escrow) на ⭐️ 30?', async (agreed) => {
      if (agreed) {
        setIsProcessing(true);
        try {
          const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
          const token = await getAuthToken(); // Запрашиваем/Достаем безопасный JWT
          
          const response = await fetch(`${API_URL}/checkout`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ action: 'checkout', itemId: 1, price: 30, source: 'WebApp' })
          });
          
          const data = await response.json();
          setIsProcessing(false);
          
          if (response.ok) {
            WebApp.showAlert(data.message);
            WebApp.HapticFeedback.notificationOccurred('success');
            // Проверяйте Telegram! Вам уже должно было прийти push-сообщение от FastAPI!
          } else {
            WebApp.showAlert(`Ошибка: ${data.detail}`);
            WebApp.HapticFeedback.notificationOccurred('error');
          }
        } catch (apiError) {
          setIsProcessing(false);
          WebApp.showAlert('Ошибка соединения с сервером.');
        }
      }
    });
  };

  return (
    <div className="flex flex-col h-full min-h-[60vh]">
      <h2 className="text-lg font-bold mb-4">🛍 Ваша корзина</h2>
      
      <div className="flex-1 space-y-3">
        <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-slate-800 rounded-xl p-3 border border-slate-700 flex items-center gap-3">
          <div className="w-16 h-16 bg-slate-700 rounded-lg flex items-center justify-center p-2">
            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" className="w-full h-full object-contain" />
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-sm text-slate-200">Telegram Premium (1 Year)</h4>
            <span className="text-xs text-slate-400 mt-1 block">Продавец: Скрыт (Escrow Secure)</span>
            <div className="font-bold text-amber-400 mt-1 flex items-center gap-1">
              <span>⭐️</span><span>30</span>
            </div>
          </div>
        </motion.div>
      </div>

      <div className="mt-6 bg-slate-800/80 rounded-2xl p-4 border border-slate-700 backdrop-blur-sm shadow-xl">
        <div className="flex justify-between items-center mb-2">
          <span className="text-slate-400 text-sm">Итого:</span>
          <span className="text-xl font-bold text-amber-400">⭐️ 30</span>
        </div>
        
        <div className="flex items-center gap-2 mb-4 text-xs text-emerald-400 bg-emerald-400/10 p-2 rounded-lg">
          <ShieldCheck size={16} />
          <span>Защищено Escrow. Уведомление в ЛС моментально.</span>
        </div>

        <button 
          onClick={handleCheckout}
          disabled={isProcessing}
          className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-blue-500/25 flex items-center justify-center gap-2 transition-all active:scale-95"
        >
          {isProcessing ? <><Loader2 size={18} className="animate-spin" /> Подпись JWT...</> : <><ArrowRight size={18} /> Оплатить Telegram Stars</>}
        </button>
      </div>
    </div>
  );
}
