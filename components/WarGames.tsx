import React from 'react'
import { motion } from 'framer-motion'
import { Users, Trophy, Clock, Star } from 'lucide-react'

export default function WarGames() {
  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <Users className="w-16 h-16 text-green-400 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-white mb-2">War Games</h1>
        <p className="text-gray-300">Competitive cybersecurity challenges</p>
      </motion.div>
    </div>
  )
} 