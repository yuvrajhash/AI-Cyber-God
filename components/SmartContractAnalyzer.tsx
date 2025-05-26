import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Brain, Upload, AlertTriangle, CheckCircle, Clock, Shield } from 'lucide-react'

interface Vulnerability {
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  description: string
  confidence: number
}

interface AnalysisResult {
  id: string
  vulnerabilities: Vulnerability[]
  risk_score: number
  recommendations: string[]
  timestamp: string
}

export default function SmartContractAnalyzer() {
  const [contractCode, setContractCode] = useState('')
  const [contractAddress, setContractAddress] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)

  const handleAnalyze = async () => {
    if (!contractCode && !contractAddress) return

    setIsAnalyzing(true)
    
    try {
      // Simulate API call to backend
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Mock analysis result
      const mockResult: AnalysisResult = {
        id: 'analysis_' + Date.now(),
        vulnerabilities: [
          {
            type: 'reentrancy',
            severity: 'high',
            description: 'Potential reentrancy vulnerability detected in transfer function',
            confidence: 0.85
          },
          {
            type: 'integer_overflow',
            severity: 'medium',
            description: 'Unchecked arithmetic operations may lead to overflow',
            confidence: 0.72
          }
        ],
        risk_score: 0.65,
        recommendations: [
          'Implement checks-effects-interactions pattern',
          'Use SafeMath library for arithmetic operations',
          'Add reentrancy guards to sensitive functions'
        ],
        timestamp: new Date().toISOString()
      }
      
      setAnalysisResult(mockResult)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-500 bg-red-500/10 border-red-500/20'
      case 'high': return 'text-orange-500 bg-orange-500/10 border-orange-500/20'
      case 'medium': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20'
      case 'low': return 'text-green-500 bg-green-500/10 border-green-500/20'
      default: return 'text-gray-500 bg-gray-500/10 border-gray-500/20'
    }
  }

  const getRiskScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-red-400'
    if (score >= 0.6) return 'text-orange-400'
    if (score >= 0.4) return 'text-yellow-400'
    return 'text-green-400'
  }

  return (
    <div className="space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <Brain className="w-16 h-16 text-purple-400 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-white mb-2">Smart Contract Analyzer</h1>
        <p className="text-gray-300">AI-powered vulnerability detection for smart contracts</p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <h2 className="text-xl font-bold text-white mb-6">Contract Input</h2>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Contract Address (Optional)
              </label>
              <input
                type="text"
                value={contractAddress}
                onChange={(e) => setContractAddress(e.target.value)}
                placeholder="0x..."
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Contract Source Code
              </label>
              <textarea
                value={contractCode}
                onChange={(e) => setContractCode(e.target.value)}
                placeholder="pragma solidity ^0.8.0;&#10;&#10;contract MyContract {&#10;    // Your contract code here&#10;}"
                rows={12}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 font-mono text-sm"
              />
            </div>

            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || (!contractCode && !contractAddress)}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 flex items-center justify-center space-x-2"
            >
              {isAnalyzing ? (
                <>
                  <Clock className="w-5 h-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Brain className="w-5 h-5" />
                  <span>Analyze Contract</span>
                </>
              )}
            </button>
          </div>
        </motion.div>

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
        >
          <h2 className="text-xl font-bold text-white mb-6">Analysis Results</h2>
          
          {!analysisResult ? (
            <div className="text-center py-12">
              <Shield className="w-16 h-16 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400">No analysis results yet</p>
              <p className="text-gray-500 text-sm mt-2">Submit a contract to begin analysis</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Risk Score */}
              <div className="bg-gray-700/30 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-300 font-medium">Overall Risk Score</span>
                  <span className={`text-2xl font-bold ${getRiskScoreColor(analysisResult.risk_score)}`}>
                    {(analysisResult.risk_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      analysisResult.risk_score >= 0.8 ? 'bg-red-500' :
                      analysisResult.risk_score >= 0.6 ? 'bg-orange-500' :
                      analysisResult.risk_score >= 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                    }`}
                    style={{ width: `${analysisResult.risk_score * 100}%` }}
                  />
                </div>
              </div>

              {/* Vulnerabilities */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">
                  Vulnerabilities ({analysisResult.vulnerabilities.length})
                </h3>
                <div className="space-y-3">
                  {analysisResult.vulnerabilities.map((vuln, index) => (
                    <div
                      key={index}
                      className={`border rounded-lg p-4 ${getSeverityColor(vuln.severity)}`}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-medium capitalize">{vuln.type.replace('_', ' ')}</span>
                        <span className="text-xs px-2 py-1 rounded-full bg-current/20 capitalize">
                          {vuln.severity}
                        </span>
                      </div>
                      <p className="text-sm opacity-90 mb-2">{vuln.description}</p>
                      <div className="flex items-center space-x-2 text-xs">
                        <span>Confidence:</span>
                        <span className="font-medium">{(vuln.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="text-lg font-semibold text-white mb-4">Recommendations</h3>
                <div className="space-y-2">
                  {analysisResult.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                      <CheckCircle className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                      <span className="text-blue-100 text-sm">{rec}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
} 