# estool
天马资源导出到es工具

# 使用步骤
- 点上面浏览，选择要转的Roms目录（或者源代码里的Roms目录可以用来测试）
- 点下面浏览，找可以空目录，用来输出gamelist和media文件
- 点执行脚本


# gamelist.xml 文件格式说明
根据代码中的 GamelistFileParser.cpp 文件，我可以看出 gamelist.xml 是 ES-DE 前端用来存储游戏元数据的文件。以下是 gamelist.xml 的基本格式和字段说明：

## 基本结构
gamelist.xml 文件的基本结构如下：

```xml
<alternativeEmulator>
  <label>替代模拟器名称</label>
</alternativeEmulator>
<gameList>
  <game>
    <path>游戏路径</path>
    <!-- 游戏元数据字段 -->
  </game>
  <folder>
    <path>文件夹路径</path>
    <!-- 文件夹元数据字段 -->
  </folder>
  <!-- 更多游戏和文件夹条目 -->
</gameList>


 ```

```cpp

 MetaDataDecl gameDecls[] {
    // Key                 Type                 Default value      Statistic  Name in GuiMetaDataEd          Prompt in GuiMetaDataEd             Scrape
    {"name",               MD_STRING,           "",                false,     "NAME",                        "ENTER NAME",                       true},
    {"sortname",           MD_STRING,           "",                false,     "SORTNAME",                    "ENTER SORTNAME",                   false},
    {"collectionsortname", MD_STRING,           "",                false,     "CUSTOM COLLECTIONS SORTNAME", "ENTER COLLECTIONS SORTNAME",       false},
    {"desc",               MD_MULTILINE_STRING, "",                false,     "DESCRIPTION",                 "ENTER DESCRIPTION",                true},
    {"rating",             MD_RATING,           "0",               false,     "RATING",                      "ENTER RATING",                     true},
    {"releasedate",        MD_DATE,             "19700101T000000", false,     "RELEASE DATE",                "ENTER RELEASE DATE",               true},
    {"developer",          MD_STRING,           "unknown",         false,     "DEVELOPER",                   "ENTER DEVELOPER",                  true},
    {"publisher",          MD_STRING,           "unknown",         false,     "PUBLISHER",                   "ENTER PUBLISHER",                  true},
    {"genre",              MD_STRING,           "unknown",         false,     "GENRE",                       "ENTER GENRE",                      true},
    {"players",            MD_STRING,           "unknown",         false,     "PLAYERS",                     "ENTER NUMBER OF PLAYERS",          true},
    {"favorite",           MD_BOOL,             "false",           false,     "FAVORITE",                    "ENTER FAVORITE OFF/ON",            false},
    {"completed",          MD_BOOL,             "false",           false,     "COMPLETED",                   "ENTER COMPLETED OFF/ON",           false},
    {"kidgame",            MD_BOOL,             "false",           false,     "KIDGAME",                     "ENTER KIDGAME OFF/ON",             false},
    {"hidden",             MD_BOOL,             "false",           false,     "HIDDEN",                      "ENTER HIDDEN OFF/ON",              false},
    {"broken",             MD_BOOL,             "false",           false,     "BROKEN/NOT WORKING",          "ENTER BROKEN OFF/ON",              false},
    {"nogamecount",        MD_BOOL,             "false",           false,     "EXCLUDE FROM GAME COUNTER",   "ENTER DON'T COUNT AS GAME OFF/ON", false},
    {"nomultiscrape",      MD_BOOL,             "false",           false,     "EXCLUDE FROM MULTI-SCRAPER",  "ENTER NO MULTI-SCRAPE OFF/ON",     false},
    {"hidemetadata",       MD_BOOL,             "false",           false,     "HIDE METADATA FIELDS",        "ENTER HIDE METADATA OFF/ON",       false},
    {"playcount",          MD_INT,              "0",               false,     "TIMES PLAYED",                "ENTER NUMBER OF TIMES PLAYED",     false},
    {"controller",         MD_CONTROLLER,       "",                false,     "CONTROLLER",                  "SELECT CONTROLLER",                true},
    {"altemulator",        MD_ALT_EMULATOR,     "",                false,     "ALTERNATIVE EMULATOR",        "SELECT ALTERNATIVE EMULATOR",      false},
    {"lastplayed",         MD_TIME,             "0",               true,      "LAST PLAYED",                 "ENTER LAST PLAYED DATE",           false}
    };

    MetaDataDecl folderDecls[] {
    // Key            Type                 Default value      Statistic  Name in GuiMetaDataEd            Prompt in GuiMetaDataEd             Scrape
    {"name",          MD_STRING,           "",                false,     "NAME",                          "ENTER NAME",                       true},
    {"desc",          MD_MULTILINE_STRING, "",                false,     "DESCRIPTION",                   "ENTER DESCRIPTION",                true},
    {"rating",        MD_RATING,           "0",               false,     "RATING",                        "ENTER RATING",                     true},
    {"releasedate",   MD_DATE,             "19700101T000000", false,     "RELEASE DATE",                  "ENTER RELEASE DATE",               true},
    {"developer",     MD_STRING,           "unknown",         false,     "DEVELOPER",                     "ENTER DEVELOPER",                  true},
    {"publisher",     MD_STRING,           "unknown",         false,     "PUBLISHER",                     "ENTER PUBLISHER",                  true},
    {"genre",         MD_STRING,           "unknown",         false,     "GENRE",                         "ENTER GENRE",                      true},
    {"players",       MD_STRING,           "unknown",         false,     "PLAYERS",                       "ENTER NUMBER OF PLAYERS",          true},
    {"favorite",      MD_BOOL,             "false",           false,     "FAVORITE",                      "ENTER FAVORITE OFF/ON",            false},
    {"completed",     MD_BOOL,             "false",           false,     "COMPLETED",                     "ENTER COMPLETED OFF/ON",           false},
    {"kidgame",       MD_BOOL,             "false",           false,     "KIDGAME (ONLY AFFECTS BADGES)", "ENTER KIDGAME OFF/ON",             false},
    {"hidden",        MD_BOOL,             "false",           false,     "HIDDEN",                        "ENTER HIDDEN OFF/ON",              false},
    {"broken",        MD_BOOL,             "false",           false,     "BROKEN/NOT WORKING",            "ENTER BROKEN OFF/ON",              false},
    {"nomultiscrape", MD_BOOL,             "false",           false,     "EXCLUDE FROM MULTI-SCRAPER",    "ENTER NO MULTI-SCRAPE OFF/ON",     false},
    {"hidemetadata",  MD_BOOL,             "false",           false,     "HIDE METADATA FIELDS",          "ENTER HIDE METADATA OFF/ON",       false},
    {"controller",    MD_CONTROLLER,       "",                false,     "CONTROLLER",                    "SELECT CONTROLLER",                true},
    {"folderlink",    MD_FOLDER_LINK,      "",                false,     "FOLDER LINK",                   "SELECT FOLDER LINK",               false},
    {"lastplayed",    MD_TIME,             "0",               true,      "LAST PLAYED",                   "ENTER LAST PLAYED DATE",           false}
    };
```


## 主要组件
1. alternativeEmulator ：可选节点，用于指定系统的替代模拟器
   
   - <label> - 替代模拟器的名称，必须与 es_systems.xml 中定义的命令标签匹配
2. gameList ：主节点，包含所有游戏和文件夹条目
3. game ：表示单个游戏的节点
   
   - <path> - 游戏文件的路径（相对于系统起始路径）
   - 其他游戏元数据字段
4. folder ：表示文件夹的节点
   
   - <path> - 文件夹路径（相对于系统起始路径）
   - 其他文件夹元数据字段
## 元数据字段
从代码中可以看出，游戏和文件夹使用不同的元数据集（ GAME_METADATA 和 FOLDER_METADATA ）。虽然代码中没有直接列出所有字段，但根据解析逻辑可以推断出一些常见字段：

### 游戏元数据字段（GAME_METADATA）
- name - 游戏名称
- desc 或 description - 游戏描述
- image - 游戏图片路径
- video - 游戏视频路径
- marquee - 游戏标志图路径
- rating - 游戏评分
- releasedate - 发布日期
- developer - 开发商
- publisher - 发行商
- genre - 游戏类型
- players - 支持的玩家数量
- hidden - 是否隐藏（true/false）
### 文件夹元数据字段（FOLDER_METADATA）
- name - 文件夹名称
- 可能还有其他字段，但通常比游戏元数据少
## 特殊处理
代码中还显示了一些特殊处理：

1. 如果游戏或文件夹被标记为隐藏（ hidden ），且设置中未启用显示隐藏游戏的选项，则该条目会被完全忽略。
2. 如果 gamelist.xml 中的路径不存在，且未设置"仅信任 gamelist"选项，则该条目会被跳过。
3. 如果文件扩展名不在系统配置的搜索扩展名列表中，则该条目会被忽略。
4. 如果节点只包含默认名称（即与文件名相同的名称），则在保存时会省略该节点。
这个文件格式允许 ES-DE 前端存储和管理游戏的详细信息，以便在用户界面中显示丰富的游戏元数据。

### 官方帮助文档
https://gitlab.com/es-de/emulationstation-de/-/blob/master/INSTALL.md#es_systemsxml
