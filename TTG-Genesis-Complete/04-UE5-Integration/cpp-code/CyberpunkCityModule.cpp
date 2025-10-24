#include "CyberpunkCityModule.h"

#define LOCTEXT_NAMESPACE "FCyberpunkCityModule"

void FCyberpunkCityModule::StartupModule()
{
    // This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
    UE_LOG(LogTemp, Warning, TEXT("CyberpunkCity Module Started"));
}

void FCyberpunkCityModule::ShutdownModule()
{
    // This function may be called during shutdown to clean up your module. For modules that support dynamic reloading,
    // we call this function before unloading the module.
    UE_LOG(LogTemp, Warning, TEXT("CyberpunkCity Module Shutdown"));
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FCyberpunkCityModule, CyberpunkCity)