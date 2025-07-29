<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KaliSoft AI - Intelligent Automation</title>
    
    <!-- Tailwind CSS for modern styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts: Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap" rel="stylesheet">
    
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        /* Custom styles to supplement Tailwind */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f8; /* A very light grey-blue background */
        }

        .main-container {
            /* A light, refreshing gradient */
            background-image: linear-gradient(135deg, #e0f7fa 0%, #d1c4e9 100%);
        }
        
        .use-case-card {
            background-color: rgba(255, 255, 255, 0.7);
            transition: all 0.3s ease-in-out;
            backdrop-filter: blur(5px);
        }

        .use-case-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        
        .cta-button {
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .cta-button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 5px 15px rgba(8, 49, 112, 0.3);
        }

    </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-4 md:p-8">

    <!-- Main Banner Section -->
    <div class="main-container w-full max-w-6xl rounded-3xl p-8 md:p-12 text-gray-800 shadow-2xl mb-8">
        <div class="flex flex-col md:flex-row items-center justify-between">
            
            <!-- Left Content Column -->
            <div class="md:w-1/2 text-center md:text-left">
                <img src="http://googleusercontent.com/file_content/1" alt="KalisoftAI Logo" class="h-12 mb-6 mx-auto md:mx-0">
                
                <h1 class="text-4xl md:text-5xl font-black leading-tight tracking-tight mb-4 text-gray-900">
                    Build & Deploy AI Agents for Your Business
                </h1>

                <p class="text-lg md:text-xl max-w-xl mb-8 text-gray-600 font-light">
                    From automating internal workflows to creating intelligent marketing tools, we provide end-to-end AI solutions.
                </p>

                <a href="https://www.kalisoftai.in/" target="_blank" rel="noopener noreferrer" class="cta-button bg-indigo-600 text-white font-bold py-4 px-10 rounded-lg text-lg inline-block">
                    Discover What's Possible
                </a>
            </div>

            <!-- Right Image Column -->
            <div class="md:w-1/2 mt-8 md:mt-0 flex justify-center">
                <img src="http://googleusercontent.com/file_content/3" alt="AI Agent Bot" class="w-64 md:w-80">
            </div>
        </div>
    </div>

    <!-- Use Cases Section -->
    <div class="w-full max-w-6xl">
        <h2 class="text-3xl font-bold text-center mb-8 text-gray-800">Our Capabilities</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            
            <!-- Use Case 1: Internal Tool Automation -->
            <div class="use-case-card rounded-2xl p-6 border border-gray-200 shadow-lg">
                <div class="flex items-center text-indigo-600 mb-3">
                    <i class="fas fa-cogs fa-2x mr-4"></i>
                    <h3 class="text-xl font-bold">Internal Tool Automation</h3>
                </div>
                <p class="text-gray-600">
                    We build custom tools that parse POs from Gmail, use Gemini AI to determine material needs, and manage inventory status via an internal role-based UI.
                </p>
            </div>

            <!-- Use Case 2: Content Generation -->
            <div class="use-case-card rounded-2xl p-6 border border-gray-200 shadow-lg">
                <div class="flex items-center text-indigo-600 mb-3">
                    <i class="fas fa-video fa-2x mr-4"></i>
                    <h3 class="text-xl font-bold">AI Content Generation</h3>
                </div>
                <p class="text-gray-600">
                    Automatically generate engaging YouTube Shorts from long-form videos or create compelling video ads from static product images using our VideoCraft AI.
                </p>
            </div>

            <!-- Use Case 3: Workflow & DeFi -->
            <div class="use-case-card rounded-2xl p-6 border border-gray-200 shadow-lg">
                 <div class="flex items-center text-indigo-600 mb-3">
                    <i class="fas fa-project-diagram fa-2x mr-4"></i>
                    <h3 class="text-xl font-bold">n8n & DeFi Workflows</h3>
                </div>
                <p class="text-gray-600">
                    We design and implement complex n8n workflows for process automation and have the capability to integrate with DeFi protocols for financial applications.
                </p>
            </div>
        </div>
    </div>

</body>
</html>
