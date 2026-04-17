import { motion } from 'framer-motion';

const MOCK_ITEMS = [
  { id: 1, title: 'Telegram Premium (1 Year)', price: 29.99, category: 'Services', image: 'https://cdn-icons-png.flaticon.com/512/2111/2111646.png' },
  { id: 2, title: 'Web Development Course', price: 99.00, category: 'Education', image: 'https://cdn-icons-png.flaticon.com/512/1183/1183672.png' },
  { id: 3, title: 'Custom Avatar NFT', price: 45.50, category: 'Digital Arts', image: 'https://cdn-icons-png.flaticon.com/512/6298/6298900.png' },
];

export function Marketplace() {
  return (
    <div className="space-y-4">
      {/* Categories */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
        {['All', 'Services', 'Education', 'Digital Arts'].map((cat, i) => (
          <button key={i} className={`px-4 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${i === 0 ? 'bg-blue-500 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}>
            {cat}
          </button>
        ))}
      </div>

      {/* Grid of Cards */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {MOCK_ITEMS.map((item, index) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            key={item.id} 
            className="bg-slate-800 rounded-2xl p-3 border border-slate-700/50 shadow-sm flex flex-col gap-2 relative overflow-hidden group"
          >
            <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 blur-xl rounded-full translate-x-1/2 -translate-y-1/2 group-hover:bg-blue-500/20 transition-colors" />
            
            <div className="aspect-square bg-slate-700/50 rounded-xl flex items-center justify-center p-4">
              <img src={item.image} alt={item.title} className="w-16 h-16 object-contain drop-shadow-lg" />
            </div>
            
            <div className="flex-1 flex flex-col">
              <span className="text-[10px] text-blue-400 font-semibold uppercase tracking-wider">{item.category}</span>
              <h3 className="text-sm font-medium leading-tight mt-1 line-clamp-2">{item.title}</h3>
              <div className="mt-auto pt-3 flex items-center justify-between">
                <span className="font-bold">${item.price}</span>
                <button className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center hover:bg-blue-400 transition-colors shadow-lg shadow-blue-500/20">
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
