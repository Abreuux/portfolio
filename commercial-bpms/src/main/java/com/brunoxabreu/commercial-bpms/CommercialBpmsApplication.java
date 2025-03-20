package com.brunoxabreu.commercial_bpms;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})
public class CommercialBpmsApplication {
    public static void main(String[] args) {
        SpringApplication.run(CommercialBpmsApplication.class, args);
    }
} 