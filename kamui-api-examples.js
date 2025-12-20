/**
 * Kamui Code API 使用示例 - Node.js 版本

 * 此文件展示了如何使用 Kamui Code API 端点：
 * - t2i-kamui-fal-nano-banana-pro: 文本生成图像
 * - i2i-kamui-fal-nano-banana-pro-edit: 图像编辑

 * 安装依赖：npm install axios
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

// 加载配置文件
const config = JSON.parse(fs.readFileSync('kamui-api-config.json', 'utf-8'));

class KamuiAPI {
    constructor() {
        this.endpoints = config.endpoints;
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }

    /**
     * 使用文本生成图像
     *
     * @param {Object} params - 参数对象
     * @param {string} params.prompt - 描述要生成图像的文本提示
     * @param {number} params.numImages - 要生成的图像数量 (1-4)
     * @param {string} params.aspectRatio - 图像宽高比 ("21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16")
     * @param {string} params.outputFormat - 输出格式 ("jpeg", "png", "webp")
     * @param {boolean} params.syncMode - 是否同步运行
     * @param {boolean} params.limitGenerations - 是否限制生成数量
     * @returns {Promise<Object>} API 响应
     */
    async generateImage({
        prompt,
        numImages = 1,
        aspectRatio = "1:1",
        outputFormat = "webp",
        syncMode = false,
        limitGenerations = false
    }) {
        const endpoint = this.endpoints["t2i-kamui-fal-nano-banana-pro"];

        const payload = {
            prompt,
            num_images: numImages,
            aspect_ratio: aspectRatio,
            output_format: outputFormat,
            sync_mode: syncMode,
            limit_generations: limitGenerations
        };

        const headers = { ...this.defaultHeaders, ...endpoint.headers };

        try {
            const response = await axios.post(endpoint.url, payload, { headers });
            return response.data;
        } catch (error) {
            return {
                error: error.response?.data || error.message
            };
        }
    }

    /**
     * 编辑图像
     *
     * @param {Object} params - 参数对象
     * @param {string} params.prompt - 描述要进行的编辑的文本提示
     * @param {string} params.imageUrl - 要编辑的图像URL
     * @param {string} [params.imageUrl2] - 可选的第二张图像URL，用于复杂编辑
     * @param {number} params.numImages - 要生成的图像数量 (1-4)
     * @param {string} params.aspectRatio - 图像宽高比 ("auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16")
     * @param {string} params.outputFormat - 输出格式 ("jpeg", "png", "webp")
     * @param {boolean} params.syncMode - 是否同步运行
     * @param {boolean} params.limitGenerations - 是否限制生成数量
     * @returns {Promise<Object>} API 响应
     */
    async editImage({
        prompt,
        imageUrl,
        imageUrl2,
        numImages = 1,
        aspectRatio = "auto",
        outputFormat = "webp",
        syncMode = false,
        limitGenerations = false
    }) {
        const endpoint = this.endpoints["i2i-kamui-fal-nano-banana-pro-edit"];

        const payload = {
            prompt,
            image_url: imageUrl,
            num_images: numImages,
            aspect_ratio: aspectRatio,
            output_format: outputFormat,
            sync_mode: syncMode,
            limit_generations: limitGenerations
        };

        if (imageUrl2) {
            payload.image_url2 = imageUrl2;
        }

        const headers = { ...this.defaultHeaders, ...endpoint.headers };

        try {
            const response = await axios.post(endpoint.url, payload, { headers });
            return response.data;
        } catch (error) {
            return {
                error: error.response?.data || error.message
            };
        }
    }
}

// 异步运行示例
async function runExamples() {
    // 初始化 API 客户端
    const api = new KamuiAPI();

    // 示例 1: 文本生成图像
    console.log("=== 文本生成图像示例 ===");
    const t2iResult = await api.generateImage({
        prompt: "A beautiful sunset over mountains with a lake, anime style",
        numImages: 2,
        aspectRatio: "16:9",
        outputFormat: "png",
        syncMode: true
    });
    console.log(JSON.stringify(t2iResult, null, 2));

    // 示例 2: 图像编辑
    console.log("\n=== 图像编辑示例 ===");
    // 注意：你需要提供一个有效的图像URL
    const exampleImageUrl = "https://example.com/your-image.jpg";

    const i2iResult = await api.editImage({
        prompt: "Add a rainbow in the sky, make it more colorful",
        imageUrl: exampleImageUrl,
        numImages: 1,
        aspectRatio: "auto",
        outputFormat: "webp",
        syncMode: true
    });
    console.log(JSON.stringify(i2iResult, null, 2));

    // 示例 3: 生成创意艺术
    console.log("\n=== 创意艺术生成示例 ===");
    const artResult = await api.generateImage({
        prompt: "Cyberpunk city at night with neon lights, futuristic style",
        numImages: 4,
        aspectRatio: "21:9",
        outputFormat: "jpeg",
        syncMode: false,
        limitGenerations: true
    });
    console.log(JSON.stringify(artResult, null, 2));

    // 示例 4: 使用第二张图像进行复杂编辑
    console.log("\n=== 复杂图像编辑示例 ===");
    const exampleImageUrl2 = "https://example.com/your-second-image.jpg";

    const complexEditResult = await api.editImage({
        prompt: "Combine the style of the second image with the content of the first, create a hybrid artwork",
        imageUrl: exampleImageUrl,
        imageUrl2: exampleImageUrl2,
        numImages: 2,
        aspectRatio: "1:1",
        outputFormat: "png",
        syncMode: true
    });
    console.log(JSON.stringify(complexEditResult, null, 2));
}

// 导出类和运行示例
module.exports = { KamuiAPI, runExamples };

// 如果直接运行此文件，则执行示例
if (require.main === module) {
    runExamples().catch(console.error);
}