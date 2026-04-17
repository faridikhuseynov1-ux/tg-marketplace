import { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import { Marketplace } from './components/Marketplace';
import { Cart } from './components/Cart';
import { ShoppingBag, Store } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [activeTab, setActiveTab] = useState<'market' | 'cart'>('market');

  useEffect(() => {
    WebApp.ready();
    WebApp.expand();
  }, []);

  return (
    <div className="w-full min-h-screen pb-20 bg-slate-900 text-white flex flex-col">
      {/* Header */}
      <header className="p-4 flex items-center justify-between sticky top-0 z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
          TG Market
        </h1>
        <div className="text-sm font-medium px-3 py-1 bg-slate-800 rounded-full border border-slate-700">
          Баланс: $150.00
        </div>
      </header>

      {/* Main Content Area with Animations */}
      <main className="flex-1 overflow-x-hidden p-4">
        <AnimatePresence mode="wait">
          {activeTab === 'market' ? (
            <motion.div key="market" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 20 }} transition={{ duration: 0.2 }}>
              <Marketplace />
            </motion.div>
          ) : (
            <motion.div key="cart" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.2 }}>
              <Cart />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-slate-800/90 backdrop-blur-lg border-t border-slate-700 p-3 pb-safe">
        <div className="flex justify-around items-center max-w-md mx-auto">
          <button 
            onClick={() => setActiveTab('market')}
            className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'market' ? 'text-blue-400' : 'text-slate-400'}`}
          >
            <Store size={24} />
            <span className="text-[10px] font-medium uppercase tracking-wider">Маркет</span>
          </button>
          
          <div className="w-12 h-12 bg-blue-500 rounded-full flex justify-center items-center -mt-6 shadow-lg shadow-blue-500/30 text-white cursor-pointer hover:scale-105 transition-transform">
            <span className="text-2xl font-bold leading-none">+</span>
          </div>

          <button 
            onClick={() => setActiveTab('cart')}
            className={`flex flex-col items-center gap-1 transition-colors ${activeTab === 'cart' ? 'text-blue-400' : 'text-slate-400'}`}
          >
            <ShoppingBag size={24} />
            <span className="text-[10px] font-medium uppercase tracking-wider">Корзина</span>
          </button>
        </div>
      </nav>
    </div>
  );
}

export default App;
