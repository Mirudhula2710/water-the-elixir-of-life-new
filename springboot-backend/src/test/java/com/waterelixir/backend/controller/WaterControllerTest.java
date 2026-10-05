package com.waterelixir.backend.controller;
import com.waterelixir.backend.dto.ZoneDto;
import com.waterelixir.backend.service.WaterService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import java.util.Collections;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(WaterController.class)
public class WaterControllerTest {
    @Autowired private MockMvc mockMvc;
    @MockitoBean private WaterService waterService;

    @Test
    public void testGetZonesPublic() throws Exception {
        ZoneDto zone = new ZoneDto();
        zone.setId(1L);
        zone.setName("Test Zone");
        when(waterService.getZones()).thenReturn(Collections.singletonList(zone));
        
        mockMvc.perform(get("/api/zones"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Test Zone"));
    }
}
