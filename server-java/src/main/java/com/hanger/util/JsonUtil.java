package com.hanger.util;

import com.alibaba.fastjson.JSON;
import com.hanger.entity.Problem;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Field;
import java.util.HashMap;

/**
 * @author hanger
 * 2019-09-08 18:00
 */
public class JsonUtil {
    private static Logger logger = LoggerFactory.getLogger(JsonUtil.class);



    /**
     * 注意！！！！！！
     * 当类中存在多个静态方法时
     * 类中被其他静态方法调用的静态方法必须放在几个静态方法的前面
     * 否则会出现找不到需要加载的类的异常NoClassDefFoundError
     *
     * json格式校验核心程序
     * @param map 需要检验的json字符串转换对应的map
     * @param keys 要求该json字符串中必须包含的key并且该key值的非null
     * @return 是否符合条件
     */
    private static Boolean checkFormatCore(HashMap map , String [] keys) {

        for (String key : keys) {
            if ((!(map.containsKey(key))) || (map.get(key) == null)) {
                return false;
            }
        }

        return true;
    }



    /**
     * 判断json字符串中是否包含指定的key集合
     * json包含的key个数必需与keys的个数相同
     * @param json 需要检验的json字符串
     * @param keys 要求该json字符串中必须包含的key并且该key值的非null
     * @return 是否符合条件
     */
    public static Boolean checkFormatStrict(String json , String [] keys) {

        //logger.info("要检验的json:" + json);

        HashMap map = JSON.parseObject(json, HashMap.class);
        if (map.size() != keys.length) {
            logger.warn("请求体参数格式错误");
            return false;
        }

        return checkFormatCore(map , keys);
    }



    /**
     * 判断json字符串中是否包含指定的key集合
     * json包含的key个数不需要与keys的个数相同
     * @param json 需要检验的json字符串
     * @param keys 要求该json字符串中必须包含的key并且该key值的非null
     * @param maxKeyNum json字符串中允许的key的最大个数
     * @return 是否符合条件
     */
    public static Boolean checkFormat(String json , String[] keys , Integer maxKeyNum) {

        HashMap map = JSON.parseObject(json, HashMap.class);
        if (map.size() > maxKeyNum) {
            logger.warn("请求体参数格式错误");
            return false;
        }

        return checkFormatCore(map , keys);
    }



    /**
     * 判断json字符串是否包含指定javaBean的属性
     * 注：
     *  1、包含的字段名必须与实体类的对应属性字段完全相同
     *  2、结合fastJson的JSON.parseObject()使用
     *  3、包含一个Bean中的属性就可以转对应的javaBean
     *  4、Bean中不存在的属性自动忽略
     *  5、重复的属性取最后出现的值
     * @param json 需要检验的json字符串
     * @param clazz 需要检验的java类
     * @return 是否符合条件
     */
    public static Boolean checkFormat(String json , Class<Problem> clazz) {

        HashMap map = JSON.parseObject(json, HashMap.class);

        Field[] declaredFields = clazz.getDeclaredFields();
        for (Field declaredField : declaredFields) {
            if (map.containsKey(declaredField.getName())) {
                return true;
            }
        }

        return false;
    }





}
