import { motion } from 'framer-motion';
import { ShieldCheck, ArrowRight } from 'lucide-react';
import WebApp from '@twa-dev/sdk';

export function Cart() {
  const handleCheckout = () => {
    WebApp.HapticFeedback.impactOccurred('medium');
    WebApp.showConfirm('Start a secure Escrow deal for $29.99?', (agreed) => {
      if (agreed) {
        WebApp.showAlert('Deal initiated! Check your Telegram messages.');
      }
    });
  };

  return (
    <div className="flex flex-col h-full min-h-[60vh]">
      <h2 className="text-lg font-bold mb-4">Твоя корзина</h2>
      
      <div className="flex-1 space-y-3">
        <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="bg-slate-800 rounded-xl p-3 border border-slate-700 flex items-center gap-3">
          <div className="w-16 h-16 bg-slate-700 rounded-lg flex items-center justify-center p-2">
            <img src="https://cdn-icons-png.flaticon.com/512/2111/2111646.png" className="w-full h-full object-contain" />
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-sm text-slate-200">Telegram Premium (1 Year)</h4>
            <span className="text-xs text-slate-400 mt-1 block">Seller: @durov_fan</span>
            <div className="font-bold text-blue-400 mt-1">$29.99</div>
          </div>
        </motion.div>
      </div>

      <div className="mt-6 bg-slate-800/80 rounded-2xl p-4 border border-slate-700 backdrop-blur-sm">
        <div className="flex justify-between items-center mb-2">
          <span className="text-slate-400 text-sm">Итого:</span>
          <span className="text-xl font-bold">$29.99</span>
        </div>
        
        <div className="flex items-center gap-2 mb-4 text-xs text-emerald-400 bg-emerald-400/10 p-2 rounded-lg">
          <ShieldCheck size={16} />
          <span>Сделка защищена через Escrow смарт-контракт</span>
        </div>

        <button 
          onClick={handleCheckout}
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3.5 rounded-xl shadow-lg shadow-blue-500/25 flex items-center justify-center gap-2 transition-all active:scale-95"
        >
          Оплатить безопасно
          <ArrowRight size={18} />
        </button>
      </div>
    </div>
  );
}
