package com.brunoxabreu.billing_orchestrator.service;

import com.brunoxabreu.billing_orchestrator.model.Subscription;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class ProtheusService {

    @Value("${protheus.base-url}")
    private String protheusBaseUrl;

    @Value("${protheus.api-key}")
    private String protheusApiKey;

    private final RestTemplate restTemplate;
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyyMMdd");

    public ProtheusService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Transactional
    public String createOrUpdateCustomer(Subscription subscription) {
        String endpoint = protheusBaseUrl + "/api/v1/customers";
        
        Map<String, Object> customerData = new HashMap<>();
        customerData.put("code", subscription.getProtheusCustomerId());
        customerData.put("name", subscription.getCustomerId());
        customerData.put("email", subscription.getCustomerId());
        customerData.put("type", "J");
        customerData.put("status", "A");
        customerData.put("stripe_customer_id", subscription.getCustomerId());

        HttpHeaders headers = createHeaders();
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(customerData, headers);

        ResponseEntity<Map> response = restTemplate.exchange(
            endpoint,
            HttpMethod.POST,
            request,
            Map.class
        );

        return (String) response.getBody().get("code");
    }

    @Transactional
    public String createInvoice(Subscription subscription, String stripeInvoiceId) {
        String endpoint = protheusBaseUrl + "/api/v1/invoices";
        
        Map<String, Object> invoiceData = new HashMap<>();
        invoiceData.put("customer_code", subscription.getProtheusCustomerId());
        invoiceData.put("date", LocalDateTime.now().format(DATE_FORMATTER));
        invoiceData.put("due_date", subscription.getNextBillingDate().format(DATE_FORMATTER));
        invoiceData.put("amount", subscription.getAmount());
        invoiceData.put("currency", subscription.getCurrency());
        invoiceData.put("stripe_invoice_id", stripeInvoiceId);
        invoiceData.put("subscription_id", subscription.getStripeSubscriptionId());
        invoiceData.put("status", "P");

        HttpHeaders headers = createHeaders();
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(invoiceData, headers);

        ResponseEntity<Map> response = restTemplate.exchange(
            endpoint,
            HttpMethod.POST,
            request,
            Map.class
        );

        return (String) response.getBody().get("code");
    }

    @Transactional
    public void updateInvoiceStatus(String protheusInvoiceId, String status) {
        String endpoint = protheusBaseUrl + "/api/v1/invoices/" + protheusInvoiceId + "/status";
        
        Map<String, Object> statusData = new HashMap<>();
        statusData.put("status", status);

        HttpHeaders headers = createHeaders();
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(statusData, headers);

        restTemplate.exchange(
            endpoint,
            HttpMethod.PUT,
            request,
            Map.class
        );
    }

    @Transactional
    public void updateCustomerStatus(String protheusCustomerId, String status) {
        String endpoint = protheusBaseUrl + "/api/v1/customers/" + protheusCustomerId + "/status";
        
        Map<String, Object> statusData = new HashMap<>();
        statusData.put("status", status);

        HttpHeaders headers = createHeaders();
        HttpEntity<Map<String, Object>> request = new HttpEntity<>(statusData, headers);

        restTemplate.exchange(
            endpoint,
            HttpMethod.PUT,
            request,
            Map.class
        );
    }

    private HttpHeaders createHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("X-API-Key", protheusApiKey);
        return headers;
    }

    public Map<String, Object> getCustomerDetails(String protheusCustomerId) {
        String endpoint = protheusBaseUrl + "/api/v1/customers/" + protheusCustomerId;
        
        HttpHeaders headers = createHeaders();
        HttpEntity<?> request = new HttpEntity<>(headers);

        ResponseEntity<Map> response = restTemplate.exchange(
            endpoint,
            HttpMethod.GET,
            request,
            Map.class
        );

        return response.getBody();
    }

    public Map<String, Object> getInvoiceDetails(String protheusInvoiceId) {
        String endpoint = protheusBaseUrl + "/api/v1/invoices/" + protheusInvoiceId;
        
        HttpHeaders headers = createHeaders();
        HttpEntity<?> request = new HttpEntity<>(headers);

        ResponseEntity<Map> response = restTemplate.exchange(
            endpoint,
            HttpMethod.GET,
            request,
            Map.class
        );

        return response.getBody();
    }
} 