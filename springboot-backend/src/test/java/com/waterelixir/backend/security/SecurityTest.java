package com.waterelixir.backend.security;
import com.waterelixir.backend.controller.WaterController;
import com.waterelixir.backend.service.WaterService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(WaterController.class)
public class SecurityTest {
    @Autowired private MockMvc mockMvc;
    @MockitoBean private WaterService waterService;

    @Test
    public void testDeleteAlertRequiresAuth() throws Exception {
        mockMvc.perform(delete("/api/alerts/1"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "STAFF")
    public void testDeleteAlertWithStaff() throws Exception {
        mockMvc.perform(delete("/api/alerts/1"))
                .andExpect(status().isNoContent());
    }
    
    @Test
    @WithMockUser(roles = "USER")
    public void testDeleteAlertForbiddenForUser() throws Exception {
        mockMvc.perform(delete("/api/alerts/1"))
                .andExpect(status().isForbidden());
    }
}
