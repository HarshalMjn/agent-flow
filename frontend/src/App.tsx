import React, { useCallback, useState } from 'react';
import {
  ReactFlow,
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Connection,
  type Edge,
  Panel,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Bot, Zap, Code, Plus, Play, Send } from 'lucide-react';

const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Input Node', type: 'input', config: {} },
    position: { x: 250, y: 25 },
  },
  {
    id: '2',
    data: { label: 'LLM Node', type: 'llm', config: { prompt: 'Translate {{input}} to French', model: 'gpt-4o' } },
    position: { x: 250, y: 150 },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2' },
];

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const onExecute = async () => {
    console.log('Executing Workflow...', { nodes, edges });
    // Trigger backend API
  };

  return (
    <div className="flex h-screen w-full bg-slate-950">
      {/* Sidebar */}
      <div className="w-64 border-r border-slate-800 p-4 flex flex-col gap-4">
        <h1 className="text-xl font-bold bg-gradient-to-r from-sky-400 to-indigo-500 bg-clip-text text-transparent">
          Agent Flow
        </h1>
        <div className="flex flex-col gap-2 mt-4">
          <button className="flex items-center gap-2 p-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition-colors border border-slate-700">
            <Bot size={16} /> LLM Node
          </button>
          <button className="flex items-center gap-2 p-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition-colors border border-slate-700">
            <Zap size={16} /> API Node
          </button>
          <button className="flex items-center gap-2 p-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-sm transition-colors border border-slate-700">
            <Code size={16} /> Logic Node
          </button>
        </div>
        
        <div className="mt-auto">
          <button 
             onClick={onExecute}
             className="w-full flex items-center justify-center gap-2 p-3 rounded-lg bg-sky-500 hover:bg-sky-600 text-white font-semibold transition-colors shadow-lg shadow-sky-500/20"
          >
            <Play size={16} fill="currentColor" /> Run Workflow
          </button>
        </div>
      </div>

      {/* Main Flow Editor */}
      <div className="flex-1 relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          className="bg-slate-900"
        >
          <Background color="#1e293b" gap={20} />
          <Controls />
          <MiniMap nodeStrokeWidth={3} zoomable pannable />
          
          <Panel position="top-right">
             <button 
               onClick={() => setChatOpen(!chatOpen)}
               className="p-2 bg-slate-800 rounded-full border border-slate-700 hover:bg-sky-500 transition-colors"
             >
               <Send size={20} className="text-sky-400" />
             </button>
          </Panel>
        </ReactFlow>

        {/* Chat Interface (Overlay) */}
        {chatOpen && (
          <div className="absolute top-4 right-16 w-80 h-[500px] bg-slate-800 rounded-xl border border-slate-700 shadow-2xl flex flex-col z-50 overflow-hidden">
            <div className="p-4 border-b border-slate-700 font-semibold text-sky-400">Workflow Chat</div>
            <div className="flex-1 p-4 overflow-y-auto space-y-4">
              <div className="p-3 bg-slate-700 rounded-lg text-sm">
                Ready to trigger Agent Flow! Send a message to start execution.
              </div>
            </div>
            <div className="p-4 border-t border-slate-700">
               <div className="relative">
                 <input 
                   type="text" 
                   placeholder="Type a message..."
                   className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 pl-3 pr-10 text-sm focus:outline-none focus:border-sky-500"
                 />
                 <button className="absolute right-2 top-1.5 p-1 text-sky-500 hover:text-sky-400">
                   <Send size={16} />
                 </button>
               </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
