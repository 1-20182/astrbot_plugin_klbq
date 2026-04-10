"""
🌸 喵言喵语插件 ✨
═══════════════════════════════════════
💕 卡拉彼丘猫娘经典语录插件喵~
💕 随机显示卡丘猫娘经典语录喵~
💕 让你的AstrBot更加可爱喵！
═══════════════════════════════════════
🐱 开发者: 飞翔的死猪
📧 GitHub: https://github.com/1-20182/astrbot_plugin_klbq
📅 创建时间: 2026
📝 许可证: MIT
═══════════════════════════════════════

🎀 这是喵言喵语插件的入口文件，主要负责处理QQ命令功能喵~
🎀 喵~喵~喵~欢迎使用喵言喵语插件哦！"""

import asyncio
import random
import aiohttp
import json
import ast
import base64
from pathlib import Path
from datetime import datetime, timedelta

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, StarTools
from astrbot.api import logger


class MeowQuotesPlugin(Star):
    """
    🌸 喵言喵语插件
    💕 随机显示卡丘猫娘经典语录喵~
    💕 喵~喵~喵~可爱的猫娘语录等你来发现哦！
    """
    
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.context = context
        self.config = config or {}
        
        # 数据目录
        self.data_dir = Path(__file__).parent
        # 使用框架提供的数据目录存储动态数据
        self.dynamic_data_dir = StarTools.get_data_dir(self)
        
        # 喵言喵语数据
        self.meow_quotes = []
        
        # 同步更新相关
        self.last_update_time = None
        self.update_interval = timedelta(hours=1)  # 每小时检查一次更新
        # 使用国内加速站访问GitHub API
        self.github_repo_url = "https://ghproxy.com/https://api.github.com/repos/Coconut-Aero/calabiyauify-names/contents/src/data/meowQuotes.js"
        self.data_file_path = self.dynamic_data_dir / "meowQuotes.js"
        
        # 异步任务引用
        self.update_task = None
        
        logger.info("✨ [MeowQuotesPlugin] 喵言喵语插件初始化完成喵~")
    
    async def initialize(self):
        """🚀 插件初始化时调用喵~
        喵~喵~喵~开始初始化插件啦！"""
        
        try:
            # 加载喵言喵语数据喵~
            await self._load_meow_quotes()
            
            # 检查是否需要更新数据喵~
            await self._check_and_update_meow_quotes()
            
            # 启动定时更新任务喵~
            self.update_task = asyncio.create_task(self._schedule_update_task())
            
            logger.info("=" * 60)
            logger.info("✅ 喵言喵语插件启动成功喵！")
            logger.info("")
            logger.info(f"📝 已加载 {len(self.meow_quotes)} 条喵言喵语喵~")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"❌ [MeowQuotesPlugin] 启动失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    @filter.command("喵言喵语")
    async def meow_quotes(self, event: AstrMessageEvent):
        """喵言喵语指令喵~
        喵~喵~喵~随机发送一条可爱的猫娘语录哦！"""
        quote = self._get_random_quote()
        yield event.plain_result(quote)
    
    @filter.command("卡丘表情包")
    async def calabiyau_emoji(self, event: AstrMessageEvent):
        """卡丘表情包指令喵~
        喵~喵~喵~随机发送一张可爱的卡丘表情包哦！"""
        try:
            # 读取表情包文件
            emoji_files = self._get_emoji_files()
            if not emoji_files:
                yield event.plain_result("喵~没有找到表情包文件呢！")
                return
            
            # 随机选择一张表情包
            selected_emoji = random.choice(emoji_files)
            
            # 发送表情包
            yield event.image_result(str(selected_emoji))
        except Exception as e:
            logger.error(f"❌ 发送表情包失败: {e}")
            yield event.plain_result("喵~发送表情包失败了呢！")
    
    async def _load_meow_quotes(self):
        """加载喵言喵语数据喵~
        喵~喵~喵~开始加载可爱的猫娘语录啦！"""
        try:
            quotes_path = self.data_dir / "data" / "meowQuotes.js"
            if quotes_path.exists():
                content = quotes_path.read_text(encoding='utf-8')
                start = content.find('[')
                end = content.rfind(']')
                if start != -1 and end != -1:
                    array_content = content[start:end+1]
                    self.meow_quotes = ast.literal_eval(array_content)
                    logger.info(f"✅ 从文件加载了 {len(self.meow_quotes)} 条喵言喵语喵~")
                    return
            
            logger.warning("⚠️  未找到meowQuotes.js文件，使用内置数据喵~")
            self.meow_quotes = [
                "错了喵！！错了喵！别捅我喵！我变猫娘给你撅，不要捅我了喵！",
                "有情绪喵？红温了喵？喷我也没用喵！我很菜的喵！你要一打五才能赢喵！我唯一作用就是凑齐五个人开游戏喵！",
                "我们很遗憾的宣布《卡拉彼丘》将于喵年喵月喵日终止运营喵，祝您生活愉快喵！人生有梦喵，各自精彩喵",
                "虾仁饭好可怕喵！虾仁饭好可怕喵！虾仁饭好可怕喵！虾仁饭好可怕喵！虾仁饭好可怕喵！虾仁饭好可怕喵！",
                "天天在频道喵喵叫！天天在频道喵喵叫！吵死我了喵！捅似你们喵！捅似你们喵！捅似你们喵！"
            ]
        except Exception as e:
            logger.error(f"❌ 加载喵言喵语数据失败: {e}")
            self.meow_quotes = ["喵！喵！喵！欢迎使用喵言喵语插件喵！"]
    
    def _get_random_quote(self) -> str:
        """获取随机喵言喵语喵~
        喵~喵~喵~随机挑选一条可爱的猫娘语录哦！"""
        if not self.meow_quotes:
            return "喵！喵！喵！欢迎使用喵言喵语插件喵！"
        return random.choice(self.meow_quotes)
    
    def _get_emoji_files(self) -> list:
        """获取表情包文件列表喵~
        喵~喵~喵~读取emoji目录下的所有表情包文件哦！"""
        try:
            emoji_dir = self.data_dir / "emoji"
            if not emoji_dir.exists() or not emoji_dir.is_dir():
                logger.warning("⚠️  emoji目录不存在喵~")
                return []
            
            # 支持的表情包文件格式
            supported_formats = {'.gif', '.jpg', '.jpeg', '.png', '.webp'}
            emoji_files = []
            
            for file in emoji_dir.iterdir():
                if file.is_file() and file.suffix.lower() in supported_formats:
                    emoji_files.append(file)
            
            if not emoji_files:
                logger.warning("⚠️  emoji目录为空喵~")
            
            return emoji_files
        except Exception as e:
            logger.error(f"❌ 读取表情包文件失败: {e}")
            return []
    
    async def _schedule_update_task(self):
        """定时检查更新任务喵~
        喵~喵~喵~定期检查GitHub仓库的更新哦！"""
        while True:
            await asyncio.sleep(3600)  # 每小时检查一次
            await self._check_and_update_meow_quotes()
    
    async def _check_and_update_meow_quotes(self):
        """检查并更新喵言喵语数据喵~
        喵~喵~喵~检查GitHub仓库是否有更新哦！"""
        try:
            # 检查是否到了更新时间
            if self.last_update_time and datetime.now() - self.last_update_time < self.update_interval:
                return
            
            logger.info("🔍 [MeowQuotesPlugin] 检查喵言喵语数据更新喵~")
            
            # 下载最新数据
            new_quotes = await self._download_meow_quotes()
            if new_quotes:
                # 保存到本地文件
                self.data_file_path.parent.mkdir(exist_ok=True)
                with open(self.data_file_path, 'w', encoding='utf-8') as f:
                    f.write('/* =========================\n  喵言喵语数据\n  ========================= */\n\nexport const meowQuotes = ')
                    f.write(json.dumps(new_quotes, ensure_ascii=False, indent=2))
                    f.write(';')
                
                # 重新加载数据
                await self._load_meow_quotes()
                self.last_update_time = datetime.now()
                logger.info(f"✅ [MeowQuotesPlugin] 喵言喵语数据更新成功喵！现在有 {len(self.meow_quotes)} 条语录喵~")
            else:
                logger.info("ℹ️  [MeowQuotesPlugin] 喵言喵语数据已是最新喵~")
        except Exception as e:
            logger.error(f"❌ [MeowQuotesPlugin] 检查更新失败: {e}")
    
    async def _download_meow_quotes(self) -> list:
        """从GitHub下载最新的喵言喵语数据喵~
        喵~喵~喵~从GitHub仓库获取最新的猫娘语录哦！"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.github_repo_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # 解码base64内容喵~
                        content = base64.b64decode(data['content']).decode('utf-8')
                        
                        # 解析数据喵~
                        start = content.find('[')
                        end = content.rfind(']')
                        if start != -1 and end != -1:
                            array_content = content[start:end+1]
                            # 解析数组内容喵~
                            quotes = ast.literal_eval(array_content)
                            return quotes
        except Exception as e:
            logger.error(f"❌ [MeowQuotesPlugin] 下载数据失败: {e}")
        return []
    
    async def terminate(self):
        """🛑 插件关闭时调用喵~
        喵~喵~喵~插件要关闭啦，下次再见哦！"""
        # 取消异步任务，避免任务泄漏
        if self.update_task:
            self.update_task.cancel()
        logger.info("[MeowQuotesPlugin] 喵言喵语插件已关闭喵~")


__all__ = ['MeowQuotesPlugin']
