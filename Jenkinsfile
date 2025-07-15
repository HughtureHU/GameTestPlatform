// Jenkinsfile - Final Windows Agent Version
pipeline {
    // 关键改动 #1: 指定任务必须在有 'windows' 标签的代理上运行
    // Jenkins Master看到这个标签，就会把任务派发给我们的Windows Agent
    agent { label 'windows' } 

    stages {
        // 我们将所有步骤都放在一个核心的构建阶段里
        stage('Build Windows Game on Windows Agent') {
            steps {
                // bat 是在Windows代理上执行批处理命令的步骤
                echo "--- Job is now running on a Windows Agent! ---"

                echo "Verifying workspace directory..."
                // 关键改动 #2: 使用Windows的命令 'cd' (打印当前目录) 和 'dir' (列出文件)
                // Jenkins会自动把代码拉取到它在Agent上设置的工作目录（比如F:\remote_jenkins\workspace\...）
                bat 'cd' 
                bat 'dir'

                echo "--- Activating Python virtual environment and starting build script... ---"

                // 关键改动 #3: 执行我们为Windows编写的、能打包真实游戏的流程
                // 使用 '&&' 来确保只有在前一个命令成功后才执行后一个
                // 路径中的 \ 是Windows的分隔符
                bat 'call backend\\venv\\Scripts\\activate.bat && python backend\\scripts\\build_simple_shooter.py'
            }
        }
    }

    post {
        // 构建后操作
        always {
            echo '--- Pipeline finished on Windows Agent. ---'
            // 在这里，我们可以加入步骤来归档构建产物(游戏包)，或者发送通知
        }
    }
}