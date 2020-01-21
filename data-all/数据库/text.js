//列出所有数据库
show dbs

//切换到evaluate数据库
use text

// db.createCollection('problem')//问题本体
// db.createCollection('reply')//问题得回答记录

//列出所有集合
show collections

//删除集合test
// db.test.drop()

//列出对应集合的所有文档
db.problem.find()
db.reply.find()

