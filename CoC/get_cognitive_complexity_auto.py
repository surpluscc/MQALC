import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
import os

def get_cognitive_complexity(url, username, password, headless=True):
    """
    使用Selenium登录并获取Cognitive Complexity数据
    
    参数:
        url: SonarQube页面URL
        username: 登录用户名
        password: 登录密码
        headless: 是否使用无头模式（不显示浏览器窗口）
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--log-level=3')
    
    driver = None
    
    try:
        print("正在启动Chrome浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 先访问登录页面
        base_url = url.split('/component_measures')[0]
        login_url = f"{base_url}/sessions/new"
        
        print(f"正在访问登录页面: {login_url}")
        driver.get(login_url)
        time.sleep(2)
        
        # 查找并填写登录表单
        print("正在登录...")
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login"))
            )
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # 提交表单
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            print("等待登录完成...")
            time.sleep(5)
            print("登录成功！")
        except Exception as e:
            print(f"登录过程出错: {e}")
            # 保存登录页面截图
            driver.save_screenshot('login_error.png')
            return None
        
        # 访问目标页面
        print(f"\n正在访问目标页面: {url}")
        driver.get(url)
        print("等待页面加载...")
        time.sleep(8)  # 等待更长时间确保数据加载
        
        # 先滚动到页面底部，Show More按钮通常在底部
        print("\n滚动到页面底部...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 点击"Show More"按钮加载所有数据
        print("\n正在查找并点击 'Show More' 按钮...")
        click_count = 0
        max_attempts = 20  # 最多尝试20次
        
        # 先保存初始页面信息用于调试
        with open('debug_page.txt', 'w', encoding='utf-8') as f:
            body_text = driver.find_element(By.TAG_NAME, "body").text
            f.write(body_text)
            # 查找包含"more"或数字的关键行
            lines = body_text.split('\n')
            for i, line in enumerate(lines):
                if 'more' in line.lower() or ('500' in line and i < len(lines) - 10):
                    f.write(f"\n\n=== 第{i}行包含关键字 ===\n")
                    f.write(f"{lines[max(0,i-2):min(len(lines),i+3)]}\n")
        print("已保存调试信息到 debug_page.txt")
        
        while click_count < max_attempts:
            try:
                # 查找"Show More"按钮的多种可能选择器
                show_more_button = None
                
                # 尝试不同的选择器
                selectors = [
                    "//button[contains(text(), 'Show More')]",
                    "//button[contains(text(), 'show more')]",
                    "//a[contains(text(), 'Show More')]",
                    "//a[contains(text(), 'show more')]",
                    "//*[contains(text(), 'Show More')]",
                    "//*[contains(text(), 'show more')]",
                    "//button[contains(@class, 'show-more')]",
                    "//a[contains(@class, 'show-more')]",
                    "//*[contains(@class, 'show-more')]",
                    # SonarQube specific
                    "//button[contains(@class, 'button')]",
                    "//a[contains(@class, 'button')]",
                    "//*[@role='button']"
                ]
                
                for selector in selectors:
                    try:
                        buttons = driver.find_elements(By.XPATH, selector)
                        if buttons:
                            # 找到第一个可见的按钮
                            for btn in buttons:
                                if btn.is_displayed() and btn.is_enabled():
                                    show_more_button = btn
                                    break
                            if show_more_button:
                                break
                    except:
                        continue
                
                if show_more_button:
                    try:
                        # 滚动到按钮附近并等待其可点击
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_button)
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(show_more_button))
                        time.sleep(0.5)
                        
                        try:
                            show_more_button.click()
                        except Exception as click_error:
                            # 回退到JS点击，解决被遮挡/动画未完成等问题
                            print(f"普通点击失败，使用JS点击: {click_error}")
                            driver.execute_script("arguments[0].click();", show_more_button)
                        
                        click_count += 1
                        print(f"已点击 'Show More' 按钮 {click_count} 次")
                        
                        # 等待新数据加载
                        time.sleep(3)
                    except Exception as e:
                        print(f"按钮可点击检测失败: {e}")
                else:
                    # 没有找到按钮，说明所有数据已加载
                    print("未找到 'Show More' 按钮，所有数据已加载完成")
                    break
                    
            except Exception as e:
                # 按钮不可用或出错，说明数据已全部加载
                print(f"加载完成（点击了 {click_count} 次）")
                break
        
        if click_count >= max_attempts:
            print(f"已达到最大点击次数 ({max_attempts})，继续处理当前数据...")
        
        # 再等待一下确保所有数据都渲染完成
        time.sleep(3)
        print("数据加载完成，开始提取...")
        
        # 保存页面内容
        page_text = driver.find_element(By.TAG_NAME, "body").text
        with open('page_content_logged_in.txt', 'w', encoding='utf-8') as f:
            f.write(page_text)
        print("已保存登录后的页面内容到 page_content_logged_in.txt")
        
        page_html = driver.page_source
        with open('page_html_logged_in.html', 'w', encoding='utf-8') as f:
            f.write(page_html)
        print("已保存登录后的页面HTML到 page_html_logged_in.html")
        
        # 注：已禁用截图功能以避免生成临时文件
        # driver.save_screenshot('page_screenshot.png')
        # print("已保存页面截图到 page_screenshot.png")
        
        # 提取数据 - 多种方法
        results = {}
        lines = page_text.split('\n')
        
        print("\n开始解析数据...")
        print(f"页面共有 {len(lines)} 行文本")
        
        # 方法1: 查找.py文件和后续的数字
        for i, line in enumerate(lines):
            line = line.strip()
            if '.py' in line and line.endswith('.py'):
                # 检查接下来的几行是否有数字
                for j in range(1, 10):  # 检查接下来的10行
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        if next_line.isdigit():
                            results[line] = next_line
                            print(f"找到: {line} -> {next_line}")
                            break
        
        # 方法2: 使用XPath或CSS选择器查找表格数据
        print("\n尝试使用XPath查找表格数据...")
        try:
            # 查找所有包含.py的元素
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), '.py')]")
            print(f"找到 {len(elements)} 个包含.py的元素")
            
            for element in elements:
                text = element.text.strip()
                if text.endswith('.py'):
                    # 查找父元素或相邻元素中的数字
                    try:
                        parent = element.find_element(By.XPATH, "..")
                        parent_text = parent.text
                        
                        # 尝试从父元素文本中提取数字
                        parts = parent_text.split('\n')
                        for part in parts:
                            part = part.strip()
                            if part.isdigit() and text not in results:
                                results[text] = part
                                print(f"通过XPath找到: {text} -> {part}")
                                break
                    except:
                        continue
        except Exception as e:
            print(f"XPath查找失败: {e}")
        
        return results
        
    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        if driver:
            print("\n关闭浏览器...")
            driver.quit()

def main():
    # 配置参数
    base_url = "http://192.168.31.38:9000"
    page_url = ""
    username = ""
    password = ""
    
    # 是否使用无头模式（True=不显示浏览器窗口，False=显示浏览器窗口）
    use_headless = True
    
    print("="*60)
    print("SonarQube Cognitive Complexity 数据获取工具")
    print("="*60)
    print(f"\n使用账户: {username}")
    print(f"目标页面: {page_url}")
    print(f"无头模式: {'开启' if use_headless else '关闭（将显示浏览器窗口）'}\n")
    
    results = get_cognitive_complexity(page_url, username, password, headless=use_headless)
    
    # 显示结果
    if results:
        print("\n" + "="*60)
        print("Cognitive Complexity 数据:")
        print("="*60)
        
        for filename, complexity in sorted(results.items()):
            print(f"{filename}: {complexity}")
        
        # 保存结果
        with open('cognitive_complexity_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("\n" + "="*60)
        print(f"成功获取 {len(results)} 个文件的数据")
        print("结果已保存到 cognitive_complexity_results.json")
        print("="*60)
        
        # 清理临时文件
        temp_files = ['page_content_logged_in.txt', 'page_html_logged_in.html', 'page_screenshot.png']
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"已清理临时文件: {temp_file}")
                except:
                    pass
    else:
        print("\n" + "="*60)
        print("未能自动提取数据")
        print("请查看以下文件手动检查：")
        print("  - page_content_logged_in.txt (页面文本)")
        print("  - page_html_logged_in.html (页面HTML)")
        print("="*60)

if __name__ == "__main__":
    main()

