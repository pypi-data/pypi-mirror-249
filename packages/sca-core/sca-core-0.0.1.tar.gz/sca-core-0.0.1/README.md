# sense-core

sense-core目前包含的功能主要有：

1）配置解析和管理

## 安装方式

    pip install sca-core
    
当前版本是0.1.1

## 使用指南

使用
    
    import sca_core 
   
导入模块。sca_core实现上是把库里的文件都导入到__init__.py，所以不需要指定sca_core下的文件。

### 配置解析和管理
约定：项目根目录放置配置文件settings.ini，按模块label分块配置各服务模块，格式类似：

    [rabbit]
    host = 127.0.0.1
    port = 5671
    user = guest
    password = guest
    

通用配置（如log_path）放到[settings]下，[settings]建议放到配置文件最后。

程序内通过scs_core.sca_config('label','item')调用,要确保item的key是存在的，否则解析配置会抛出异常。

如果不确定item是否存在可以使用sd.config('label','item','')，不存在的item会赋默认的空值。

对于非docker部署模式，根目录可以放settings.local.ini用于本地开发使用，该文件不要提到git里。
