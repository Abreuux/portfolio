package com.brunoxabreu.billing_orchestrator;

import io.camunda.zeebe.spring.client.EnableZeebeClient;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableZeebeClient
@EnableScheduling
public class BillingOrchestratorApplication {
    public static void main(String[] args) {
        SpringApplication.run(BillingOrchestratorApplication.class, args);
    }
} 