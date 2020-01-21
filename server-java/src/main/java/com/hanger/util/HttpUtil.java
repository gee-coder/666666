package com.hanger.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * @author hanger
 * 2019-11-10 19:39
 */
public class HttpUtil {
    private static Logger logger = LoggerFactory.getLogger(HttpUtil.class);



    /**
     * 打印HttpServletRequest的uri
     * @param request 要处理的请求
     */
    public static void printUri(HttpServletRequest request) {
        logger.info("uri=" + request.getRequestURI());
    }



    /**
     * 打印HttpServletRequest的method
     * @param request 要处理的请求
     */
    public static void printMethod(HttpServletRequest request) {
        //可以这样写输出时等号右边不带{}，{}代表第二个参数的返回值
        logger.info("method={}", request.getMethod());
    }



    /**
     * 打印HttpServletRequest的protocol
     * @param request 要处理的请求
     */
    public static void printProtocol(HttpServletRequest request) {
        logger.info("protocol={}", request.getProtocol());
    }



    /**
     * 打印HttpServletRequest的contentType
     * @param request 要处理的请求
     */
    public static void printContentType(HttpServletRequest request) {
        logger.info("contentType={}", request.getContentType());
    }



    /**
     * 打印HttpServletRequest的IP和Port信息
     * @param request 要处理的请求
     */
    public static void printIPPort(HttpServletRequest request) {
        logger.info("请求者:" + request.getRemoteAddr() + ":" + request.getRemotePort());
        logger.info("处理者:" + request.getLocalAddr() + ":" + request.getLocalPort());
    }



    /**
     * 打印HttpServletRequest的session
     * @param request 要处理的请求
     */
    public static void printSession(HttpServletRequest request) {
        HttpSession session = request.getSession();
        logger.info("session:" + session.getAttribute("LOGIN_USER"));
    }



    /**
     * 从HttpServletRequest中获取所有参数并封装成HashMap返回
     * @param request 要处理的请求
     * @return 包含请求中所有参数的HashMap
     */
    public static Map<String, String> getParams(HttpServletRequest request) {
        Map<String,String> params = new HashMap<String,String>();
        Map<String,String[]> requestParams = request.getParameterMap();
        for (Iterator<String> iter = requestParams.keySet().iterator(); iter.hasNext();) {
            String name = iter.next();
            String[] values = requestParams.get(name);
            String valueStr = "";
            for (int i = 0; i < values.length; i++) {
                valueStr = (i == values.length - 1) ? valueStr + values[i]
                        : valueStr + values[i] + ",";
            }
            //乱码解决，这段代码在出现乱码时使用
            //valueStr = new String(valueStr.getBytes(StandardCharsets.ISO_8859_1), StandardCharsets.UTF_8);
            params.put(name, valueStr);
        }
        return params;
    }



}
